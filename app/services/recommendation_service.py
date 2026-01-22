"""
Fault-Tolerant Recommendation Service
------------------------------------
Production reliability guarantees:
- Never crashes on bad data
- Never leaks partial failures
- Always returns a valid response
- Graceful degradation under failure
"""

from datetime import datetime, timedelta
from typing import List
import logging

import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.blog import Blog
from app.models.blog_keyword import BlogKeyword
from app.models.blog_vector import BlogVector
from app.models.user_keyword import UserKeyword

from app.services.like_service import get_liked_blogs_by_user
from app.services.comment_service import get_commented_blogs_by_user
from app.services.follow_service import get_followed_users


# ============================================================
# 🔧 CONFIG
# ============================================================

MAX_TOP_K = 50
MAX_KEYWORDS = 10
VECTOR_DOT_EPS = 1e-9

logger = logging.getLogger(__name__)


# ============================================================
# 🧼 SAFE KEYWORD EXTRACTION
# ============================================================

def extract_safe_keywords(texts: List[str]) -> List[str]:
    keywords = set()

    try:
        for text in texts:
            if not text:
                continue

            for token in text.lower().split():
                if token.isalpha() and 3 <= len(token) <= 32:
                    keywords.add(token)

                if len(keywords) >= MAX_KEYWORDS:
                    break
    except Exception:
        logger.exception("Keyword extraction failed")

    return list(keywords)


# ============================================================
# 🔍 SAFE CANDIDATE RETRIEVAL
# ============================================================

def get_candidate_blogs(
    db: Session,
    keywords: List[str],
    exclude_ids: List[int],
    limit: int = 500
) -> List[Blog]:

    if not keywords:
        return []

    try:
        blog_ids = (
            db.query(BlogKeyword.blog_id)
            .filter(BlogKeyword.keyword.in_(keywords))
            .subquery()
        )

        return (
            db.query(Blog)
            .filter(
                Blog.id.in_(blog_ids),
                ~Blog.id.in_(exclude_ids),
                Blog.is_deleted == False
            )
            .order_by(Blog.created_at.desc())
            .limit(limit)
            .all()
        )

    except SQLAlchemyError:
        logger.exception("Candidate blog query failed")
        return []


# ============================================================
# 🧠 SAFE USER VECTOR BUILD
# ============================================================

def build_user_vector(
    db: Session,
    user_id: int
) -> np.ndarray | None:

    try:
        keywords = (
            db.query(UserKeyword)
            .filter_by(user_id=user_id)
            .all()
        )
    except SQLAlchemyError:
        logger.exception("Failed to load user keywords")
        return None

    vectors = []
    weights = []

    for kw in keywords:
        try:
            vec = (
                db.query(BlogVector.vector)
                .filter_by(keyword=kw.keyword)
                .scalar()
            )
            if vec is not None:
                arr = np.array(vec, dtype=float)
                vectors.append(arr)
                weights.append(kw.weight)
        except Exception:
            logger.warning("Invalid vector for keyword=%s", kw.keyword)

    if not vectors:
        return None

    try:
        user_vec = np.average(vectors, axis=0, weights=weights)
        norm = np.linalg.norm(user_vec)
        return user_vec / (norm + VECTOR_DOT_EPS)
    except Exception:
        logger.exception("User vector normalization failed")
        return None


# ============================================================
# 🔐 MAIN ENTRY POINT (FAULT-TOLERANT)
# ============================================================

def get_recommendations(
    *,
    db: Session,
    current_user,
    top_k: int = 10
) -> List[Blog]:

    top_k = max(1, min(top_k, MAX_TOP_K))
    user_id = current_user.id

    try:
        # ----------------------------
        # Load user context
        # ----------------------------
        liked = get_liked_blogs_by_user(db, user_id)
        commented = get_commented_blogs_by_user(db, user_id)
        followed = set(get_followed_users(db, user_id) or [])

        interacted = liked + commented
        exclude_ids = [b.id for b in interacted]

        texts = [b.content for b in interacted if b.content]
        keywords = extract_safe_keywords(texts)

        # ----------------------------
        # Candidate pool
        # ----------------------------
        candidates = get_candidate_blogs(
            db=db,
            keywords=keywords,
            exclude_ids=exclude_ids
        )

        if not candidates:
            raise RuntimeError("No candidates found")

        # ----------------------------
        # Ranking
        # ----------------------------
        user_vec = build_user_vector(db, user_id)
        if user_vec is None:
            raise RuntimeError("User vector unavailable")

        vectors = {
            v.blog_id: np.array(v.vector, dtype=float)
            for v in db.query(BlogVector)
            .filter(BlogVector.blog_id.in_([b.id for b in candidates]))
            .all()
            if v.vector is not None
        }

        scored = []
        for blog in candidates:
            vec = vectors.get(blog.id)
            if vec is None or vec.shape != user_vec.shape:
                score = 0.0
            else:
                score = float(np.dot(user_vec, vec))

            if blog.author_id in followed:
                score *= 1.1

            scored.append((blog, score))

        scored.sort(key=lambda x: x[1], reverse=True)

        return [blog for blog, _ in scored[:top_k]]

    except Exception:
        # ----------------------------
        # LAST-RESORT FALLBACK
        # ----------------------------
        logger.exception("Recommendation pipeline failed — using fallback")

        try:
            fallback = (
                db.query(Blog)
                .filter(Blog.is_deleted == False)
                .order_by(Blog.created_at.desc())
                .limit(top_k)
                .all()
            )
            return fallback
        except Exception:
            logger.critical("Fallback feed failed")
            return []

import secrets
from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from sqlalchemy import text, func, TIMESTAMP
from sqlalchemy.orm import deferred

db = SQLAlchemy()


class APIKey(db.Model):
    __tablename__ = 'api_keys'
    __table_args__ = {"schema": "conf"}

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)  # descriptive name for the key
    created_by = db.Column(db.String(255), nullable=False)  # user who created the key
    created_at = db.Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    expires_at = db.Column(db.DateTime, nullable=True)  # optional expiration
    last_used_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    allowed_endpoints = db.Column(db.JSON, nullable=True)  # list of allowed endpoints/patterns

    @staticmethod
    def generate_key():
        """Generate a random API key"""
        return secrets.token_urlsafe(32)

    @staticmethod
    def get_active_key(api_key):
        """Get an active API key"""
        return APIKey.query.filter_by(
            key=api_key,
            is_active=True
        ).filter(
            or_(
                APIKey.expires_at.is_(None),
                APIKey.expires_at > datetime.now(timezone.utc)
            )
        ).first()

    def update_last_used(self):
        """Update the last used timestamp"""
        self.last_used_at = datetime.now(timezone.utc)
        db.session.commit()

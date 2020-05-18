from app import db

class TokenBlacklist(db.Model):
    __tablename__   = 'token_blacklist'
    id              = db.Column(db.INTEGER, primary_key=True)
    jti             = db.Column(db.String(36), nullable=False)
    token_type      = db.Column(db.String(10), nullable=False)
    user_identity   = db.Column(db.String(50), nullable=False)
    revoked         = db.Column(db.BOOLEAN, nullable=False)
    expires         = db.Column(db.DATETIME, nullable=False)

    def to_dict(self):
        return {
            'token_id'      : self.id,
            'jti'           : self.jti,
            'token_type'    : self.token_type,
            'user_identity' : self.user_identity,
            'revoked'       : self.revoked,
            'expires'       : self.expires
        }
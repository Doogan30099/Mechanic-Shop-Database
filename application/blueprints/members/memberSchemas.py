from application.extensions import ma
from application.models import Member


class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)


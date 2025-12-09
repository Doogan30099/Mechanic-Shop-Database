from application.extensions import ma
from application.models import Customer, Login


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

class LoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Login

login_schema = LoginSchema()
login_schemas = LoginSchema(many=True)
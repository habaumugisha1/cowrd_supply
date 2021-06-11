from src.db_setup import db
from sqlalchemy.dialects.postgresql import JSON,  UUID
from datetime import datetime
import uuid

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    zipCode = db.Column(db.String(100), nullable=False)
    addressLine1 = db.Column(db.String(100), nullable=False)
    addressLine2 = db.Column(db.String(100))
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    userRole = db.Column(db.String(50), default='lender')
    investments = db.relationship("Investment", backref="user", lazy="select", cascade="all, delete")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'firstName':self.firstName,
            'lastName':self.lastName,
            # 'password':self.password,
            'phone':self.phone,
            'country':self.country,
            'city':self.city,
            'zipCode':self.zipCode,
            'addressLine1':self.addressLine1,
            'addressLine2':self.addressLine2,
            'registered_at':self.registered_at,
            'userRole':self.userRole
        }

    def __repr__(self):
        return "<User {}>".format(self.username)

class Testimonial(db.Model):
    __tablename__ = 'testimonials'
    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = db.Column(db.String(), name=False)
    image = db.Column(db.String(), nullable=False)
    shortDescription = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    product_category = db.relationship("ProductCategory", backref="testimonials", lazy="select")
    causes = db.relationship("Cause", backref="testimonials", lazy="select")
    purchaseOrders = db.relationship("PurchaseOrder", backref="testimonials", lazy="select", cascade="all, delete")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'shortDescription':self.shortDescription,
            'description':self.description,
        }

    def __repr__(self):
        return "<User {}>".format(self.name)

class Cause(db.Model):
    __tablename__ = 'causes'

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    shortDescription = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    testmonialId = db.Column(UUID(as_uuid=True), db.ForeignKey("testimonials.id"), nullable=False)
    categories = db.relationship("ProductCategory", backref="disease", lazy="select", cascade="all, delete")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'shortDescription':self.shortDescription,
            'description':self.description,
            'testmonialId':self.testmonialId,
        }

    def __repr__(self):
        return "<Cause {}>".format(self.name)

class ProductCategory(db.Model):
    __tablename__ = 'product_category'

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=False)
    causeId = db.Column(UUID(as_uuid=True), db.ForeignKey("causes.id"), nullable=False)
    interestRate = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    fundingLimit = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(), nullable=False)
    shortDescription = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    ranking = db.Column(db.String(50), nullable=False)
    testmonialId = db.Column(UUID(as_uuid=True), db.ForeignKey("testimonials.id"), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'causeId':self.causeId,
            'interestRate':self.interestRate,
            'duration':self.duration,
            'fundingLimit':self.fundingLimit,
            'image': self.image,
            'shortDescription':self.shortDescription,
            'description':self.description,
            'ranking':self.ranking,
            'testmonialId':self.testmonialId,
        }

    def __repr__(self):
        return "<CategoryLongTerm {}>".format(self.name)

class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_order'

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    interestRate = db.Column(db.Integer, nullable=False)
    image= db.Column(db.String(), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    fundingLimit = db.Column(db.Integer, nullable=False)
    shortDescription = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    ranking = db.Column(db.String(50), nullable=False)
    testmonialId = db.Column(UUID(as_uuid=True), db.ForeignKey("testimonials.id"), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'interestRate':self.interestRate,
            'duration':self.duration,
            'fundingLimit':self.fundingLimit,
            'image': self.image,
            'shortDescription':self.shortDescription,
            'description':self.description,
            'ranking':self.ranking,
            'testmonialId':self.testmonialId,
        }

    def __repr__(self):
        return "<ShortTermDeal {}>".format(self.name)

class Investment(db.Model):
    __tablename__ = 'investments'

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    userId = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    invested_at = db.Column(db.DateTime, default=datetime.utcnow)
    productCategoryId = db.Column(UUID(as_uuid=True), nullable=False)
    amount = db.Column(db.Float(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    interestRate = db.Column(db.Integer, nullable=False)
    supplyStatus = db.Column(db.String(), default='not supplied' )
    productCategory = db.Column(db.Boolean(), default=False, nullable=False)
    purchase_order = db.Column(db.Boolean(), default=False, nullable=False)
    InvestmentStatus = db.Column(db.String(), default='pending')
    paymentStatus = db.Column(db.String(), default='Not paied')
    payment_at = db.Column(db.DateTime)
    steps = db.relationship("SupplyStatus", backref="investments", lazy="select", cascade="all, delete")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'interestRate':self.interestRate,
            'amout':self.amount,
            'invested_at':self.invested_at,
            'supplyStatus':self.supplyStatus,
            'productCategory': self.productCategory,
            'purchase_order':self.purchase_order,
            'InvestmentStatus':self.InvestmentStatus,
            'paymentStatus':self.paymentStatus,
            'productCategoryId':self.productCategoryId,
            'userId':self.userId,
        }

    

    def __repr__(self):
        return "<Investment {}>".format(self.name)

#This is for tracking the steps of any supplies of investments
class SupplyStatus(db.Model):
    __tablename__ = 'supply_status'

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    investmentId = db.Column(UUID(as_uuid=True), db.ForeignKey('investments.id'), nullable=False)
    step = db.Column(db.String(), nullable=False)
    value = db.Column(db.Integer, default=1)
    description = db.Column(db.String(), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'step': self.step,
            'investmentId':self.investmentId,
            'value':self.value,
            'description':self.description,
        }

    def __repr__(self):
        return "<SupplyStatus {}>".format(self.step)

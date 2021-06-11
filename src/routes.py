from .authentication.signup import Signup
from .authentication.get_all_users import GetAllUsers
from .authentication.login import Login, Logout
from .testimonials.testimonial import Testimonials, UpdateTestimonial
from .causes.cause import Causes, ModifyCause
from .productCategories.product_category import ProductCategoryController, productCategoryModify
from .purchaseOrder.purchase_order import PurchaseOrderController, PurchaseOrderControllerModify
from .investments.investment import InvestmentController, InvestmentAdmin, MyInvestments, MyInvestment
from .supplySteps.supply_steps import SupplyStatusController
from src.authentication.adminuser import AdminUser

def initialize_routes(api):
    # There are routes
    api.add_resource(Signup, '/api/v1/auth/signup')
    api.add_resource(GetAllUsers, '/api/v1/users')
    api.add_resource(Login, '/api/v1/auth/login')
    api.add_resource(Logout, '/api/v1/auth/logout')

    api.add_resource(Testimonials, '/api/v1/testimonial')
    api.add_resource(UpdateTestimonial, '/api/v1/testimonial/<id>')

    # causes (diseases)
    api.add_resource(Causes, '/api/v1/causes')
    api.add_resource(ModifyCause, '/api/v1/causes/<id>')

    # product category
    api.add_resource(ProductCategoryController, '/api/v1/productcategory')
    api.add_resource(productCategoryModify, '/api/v1/productcategory/<id>')

    # purchase order
    api.add_resource(PurchaseOrderController, '/api/v1/purchaseorder')
    api.add_resource(PurchaseOrderControllerModify, '/api/v1/purchaseorder/<id>')

    # investments routes
    api.add_resource(InvestmentController, '/api/v1/investment')
    api.add_resource(InvestmentAdmin, '/api/v1/investment/admin/<id>')
    api.add_resource(MyInvestments, '/api/v1/investment/myinvestments')
    api.add_resource(MyInvestment, '/api/v1/investment/myinvestments/<id>')
    api.add_resource(SupplyStatusController, '/api/v1/investment/myinvestments/<id>/supplystatus')
    api.add_resource(AdminUser, '/api/v1/auth/adminuser')
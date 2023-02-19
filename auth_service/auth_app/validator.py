from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from marshmallow.fields import Nested

from auth_app.utils import REGEX_PHONE_NUMBER, REGEX_EMAIL, REGEX_OTP, \
    REGEX_FULLNAME_VIETNAMESE, REGEX_ADDRESS_VIETNAMESE, RE_ONLY_NUMBER_AND_DASH, REGEX_VALID_PASSWORD, \
    RE_ONLY_CHARACTERS, check_format_email


class UploadValidation(Schema):
    """
    Validator
    Ex:
    {
        "file_name": "default_avatars.png",
        "prefix": "avatars"
    }
    """
    file_name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    prefix = fields.String(required=True,
                           validate=validate.OneOf(
                               choices=["avatars", "category", "manufacturer", "model", "document", "product",
                                        "article", "banner"],
                               error="Prefix must be one of "
                                     "[avatars, category, manufacturer, model, product, document, banner or article]"))


class IndexValidation(Schema):
    """
    Validator index user in excel file
    :param
        index: number
    Ex:
    {
        "index": 13
    }
    """
    index = fields.Number(required=True, validate=validate.Range(min=0, max=10000))


class AuthValidation(Schema):
    """
    Validator auth
    :param
        email: string, optional
        password: string, optional
        phone: string, optional
        otp: string, optional
    Ex:
    {
        "email": "superadmin@mayno.vn",
        "password": "admin"
    }
    """
    email = fields.String(required=False, validate=[validate.Length(min=1, max=50), validate.Regexp(REGEX_EMAIL)])
    password = fields.String(required=False,
                             validate=[validate.Length(min=1, max=16), validate.Regexp(REGEX_VALID_PASSWORD)])
    phone = fields.String(required=False,
                          validate=[validate.Length(min=1, max=20), validate.Regexp(REGEX_PHONE_NUMBER)])
    otp = fields.String(required=False, validate=[validate.Length(min=1, max=6), validate.Regexp(REGEX_OTP)])

    @validates_schema
    def validate_multi_method(self, data, **kwargs):
        if data.get('phone', None):
            if not data.get('password', None) and not data.get('otp', None):
                raise ValidationError("Missing OTP or password fields")
        elif data.get('email', None):
            if not data.get('password', None):
                raise ValidationError("Missing password field")


class SendOTPValidation(Schema):
    """
    Validator auth
    :param
        phone: string, required
    Ex:
    {
        "phone": "84909323123"
    }
    """
    phone = fields.String(required=True,
                          validate=[validate.Length(min=1, max=20), validate.Regexp(REGEX_PHONE_NUMBER)])


class CreateUserValidation(Schema):
    """
    Validator
    :param
        email: string, required
        full_name: string, required
        permission_group_id: string, required
        is_active: bool, option
    Ex:
    {
        "email": "superadmin@mayno.vn",
        "password": "admin",
        "is_admin": true
    }
    """
    email = fields.String(required=True, validate=[validate.Length(min=1, max=50), validate.Regexp(REGEX_EMAIL)])
    full_name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    permission_group_id = fields.String(required=True, validate=validate.Length(max=255))
    is_active = fields.Boolean(required=True)


class MessageSchema(Schema):
    id = fields.String()
    description = fields.String()
    show = fields.Boolean()
    duration = fields.Integer()
    status = fields.String()
    message = fields.String()


class SignupUserSchema(Schema):
    """
    Validator
    :param
        email: string, required
        password: string, required
    Ex:
    {
        "email": "sy123456@gmail.com",
        "password": "12345678aA@"
    }
    """
    email = fields.String(required=True, validate=validate.Length(min=1, max=50))
    password = fields.String(required=True, validate=validate.Length(min=1, max=50))


class RegisterCheckOPTSchema(Schema):
    """
    Validator
    :param
        opt: string, required
        user_id: string, required
    Ex:
    {
        "opt": "123456",
        "user_id": "e86bba9a-2a8e-11ec-a9c7-0a58a9feac02"
    }
    """
    otp = fields.String(required=True, validate=validate.Length(min=1, max=10))
    user_id = fields.String(required=True, validate=validate.Length(min=1, max=60))


class PasswordInitializationSchema(Schema):
    """
    Validator
    :param
        password: string, required
        user_id: string, required
    Ex:
    {
        "password": "123456",
        "user_id": "e86bba9a-2a8e-11ec-a9c7-0a58a9feac02"
    }
    """
    password = fields.String(required=True, validate=validate.Length(min=1, max=16))
    user_id = fields.String(required=True, validate=validate.Length(min=1, max=60))


class PasswordValidation(Schema):
    """
    Validator
    :param
        password: string, required
    Ex:
    {
        "password": "Admin@1234"
    }
    """
    password = fields.String(required=True,
                             validate=[validate.Length(min=1, max=16), validate.Regexp(REGEX_VALID_PASSWORD)])


class ChangeProfileValidation(Schema):
    """
    Validator
    :param
        full_name: string, required
        gender: string, not required
        date_of_birth: string, not required
        address: string, not required
        wishlist: string, not required
        email: string, not required
    Ex:
    {
        "full_name": "123456"
        "gender": "123456"
        "date_of_birth": "123456"
        "address": "123456"
        "wishlist": "123456"
        "email": "123456"
    }
    """
    full_name = fields.String(required=True,
                              validate=[validate.Length(min=1, max=50), validate.Regexp(REGEX_FULLNAME_VIETNAMESE)])
    gender = fields.Boolean(required=False)
    date_of_birth = fields.String(required=False)
    address = fields.String(required=False)
    wishlist = fields.String(required=False)
    field_of_activity = fields.String(required=False)
    email = fields.String(required=False, validate=[validate.Length(min=0, max=50)])

    @validates_schema
    def validate_email(self, data, **kwargs):
        email = data.get('email', None)
        if email and not check_format_email(email):
            raise ValidationError("Email not valid")


class ChangePasswordValidation(Schema):
    """
    Validator
    :param
        current_password: string, required
        new_password: string, required
    Ex:
    {
        "current_password": "12345678A?a"
        "new_password": "12345678A?013"
    }
    """
    current_password = fields.String(required=True,
                                     validate=[validate.Length(min=1, max=16), validate.Regexp(REGEX_VALID_PASSWORD)])
    new_password = fields.String(required=True,
                                 validate=[validate.Length(min=1, max=16), validate.Regexp(REGEX_VALID_PASSWORD)])


class EmailValidation(Schema):
    """
    Validator
    :param
        password: string, required
    Ex:
    {
        "email": "abc@gmail.com"
    }
    """
    email = fields.String(required=True, validate=[validate.Length(min=1, max=50), validate.Regexp(REGEX_EMAIL)])


class HistorySeenValidation(Schema):
    """
    Validator
    :param
        product_id: string, required
    Ex:
    """
    product_id = fields.String(required=True, validate=validate.Length(min=1, max=50))


class UserSchema(Schema):
    """
    User Schema

    """
    id = fields.String()
    email = fields.String()
    phone = fields.String()
    gender = fields.Boolean()
    full_name = fields.String()
    address = fields.String()
    wishlist = fields.String()
    field_of_activity = fields.String()
    avatar_url = fields.String()
    date_of_birth = fields.String()
    login_failed_attempts = fields.Integer()
    force_change_password = fields.Boolean()
    created_date = fields.Number()
    modified_date = fields.Number()
    modified_date_password = fields.Number()
    is_active = fields.Boolean()
    register_status = fields.Integer()
    group_id = fields.String()
    type = fields.Number()
    order_number = fields.Number()


class SpecificationValidator(Schema):
    """
        Marshmallow Schema for Product query params validator
    """
    id = fields.String(required=True, validate=validate.Length(min=0, max=50))
    min = fields.Float(required=True)
    max = fields.Float(required=True)


class ProductQueryParamsValidator(Schema):
    """
        Marshmallow Schema for Product query params validator

    """
    page = fields.Integer(required=False)
    page_size = fields.Integer(required=False)
    category_ids = fields.List(fields.String(required=False, validate=validate.Length(min=0, max=50)))
    manufacturer_ids = fields.List(fields.String(required=False, validate=validate.Length(min=0, max=50)))
    specifications = fields.List(fields.Nested(SpecificationValidator))
    model_ids = fields.List(fields.String(required=False, validate=validate.Length(min=0, max=50)))
    sort_by = fields.String(required=False, validate=validate.OneOf(["price", "time", "sales"]))
    order = fields.String(required=False, validate=validate.OneOf(["asc", "desc"]))


class SpecificationSchema(Schema):
    """
    Marshmallow Schema

    """
    id = fields.String()
    size_symbol = fields.String()
    description = fields.String()
    value = fields.Float()
    min = fields.Number()
    max = fields.Number()


class ModelSchema(Schema):
    """
        Marshmallow Schema
        Author: LucDV
        Target: Return manufacturer name and id
    """

    id = fields.String()
    name = fields.String()
    description = fields.String()
    image_url = fields.String()
    product_count = fields.Integer()
    link_seo = fields.String()
    category_id = fields.String()
    created_date = fields.Number()
    modified_date = fields.Number()

    children = fields.List(fields.Nested(lambda: ModelSchema()))


class CategorySchema(Schema):
    """
    Marshmallow Schema

    """
    id = fields.String()
    name = fields.String()
    summary_name = fields.String()
    image_url = fields.String()
    parent_id = fields.String()
    product_count = fields.Integer()
    link_seo = fields.String()
    type = fields.Integer()
    created_date = fields.Number()
    modified_date = fields.Number()

    children = fields.List(fields.Nested(lambda: CategorySchema()))
    specifications = fields.List(fields.Nested(SpecificationSchema()))
    models = fields.List(fields.Nested(ModelSchema(exclude=["children"])))


class SpecificationValidation(Schema):
    """
    Marshmallow Schema
    Target: valida specification element
    """
    id = fields.String(validate=validate.Length(min=0, max=50))
    size_symbol = fields.String(required=True,
                                validate=[validate.Length(min=1, max=1), validate.Regexp(RE_ONLY_CHARACTERS)])
    description = fields.String(required=True, validate=validate.Length(min=1, max=50))


class CategoryValidation(Schema):
    """
    Marshmallow Schema
    Target: validate parameters of category
    """
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    image_url = fields.String(required=True, validate=validate.Length(min=1, max=250))
    parent_id = fields.String(validate=validate.Length(min=0, max=50))
    is_sure = fields.Boolean()
    specifications = fields.List(fields.Nested(SpecificationValidation()))


class ManufacturerValidation(Schema):
    """
    Marshmallow Schema
    Target: validate parameters of manufacturer
    """
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    image_url = fields.String(required=True, validate=validate.Length(min=1, max=250))


class ModelValidation(Schema):
    """
    Marshmallow Schema
    Target: validate parameters of manufacturer
    """
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    image_url = fields.String(required=True, validate=validate.Length(min=1, max=250))
    manufacturer_id = fields.String(validate=validate.Length(min=0, max=50))
    parent_id = fields.String(validate=validate.Length(min=0, max=50))
    is_sure = fields.Boolean()


class GetCategoriesValidation(Schema):
    """
    Marshmallow Schema
    Target: validate parameters of category
    """
    parent_id = fields.String(validate=validate.Length(min=0, max=50))
    name = fields.String(validate=validate.Length(min=0, max=50))


class GetManufacturerValidation(Schema):
    """
    Marshmallow Schema
    Target: validate parameters of manufacturer
    """
    name = fields.String(validate=validate.Length(min=0, max=50))


class GetModelValidation(Schema):
    """
    Marshmallow Schema
    Target: validate parameters of model
    """
    manufacturer_id = fields.String(validate=validate.Length(min=0, max=50))
    parent_id = fields.String(validate=validate.Length(min=0, max=50))
    name = fields.String(validate=validate.Length(min=0, max=50))


class GetArticleValidation(Schema):
    """
    Marshmallow Schema
    Target: validate parameters of article
    """
    page = fields.Integer(required=False)
    page_size = fields.Integer(required=False)
    from_date = fields.Integer(required=False)
    to_date = fields.Integer(required=False)
    title = fields.String(required=False, validate=validate.Length(min=0, max=50))
    is_ads = fields.Boolean(required=False)
    sort = fields.String(required=False,
                         validate=validate.OneOf(
                             ["type", "title", "link", "created_date", "modified_date", "end_date"]))
    order_by = fields.String(required=False, validate=validate.OneOf(["asc", "desc"]))


class ArticleIdsValidation(Schema):
    """
        Marshmallow Schema
        Target: validate parameters of article ids
    """
    article_ids = fields.List(fields.String(required=True, validate=validate.Length(min=0, max=50)), required=True)


class ArticleSchema(Schema):
    """
    Marshmallow Schema

    """
    id = fields.String()
    type = fields.Number()
    title = fields.String()
    link = fields.String()
    content = fields.String()
    created_date = fields.Integer()
    modified_date = fields.Number()
    start_date = fields.Integer()
    image_url = fields.String()
    is_ads = fields.Boolean()
    banner_image_url = fields.String()
    dialog_image_url = fields.String()
    end_date = fields.Number()


class GetQuestionValidation(Schema):
    """
    Marshmallow Schema
    Target: validate parameters of article
    """
    page = fields.Integer(required=False)
    page_size = fields.Integer(required=False)
    question = fields.String(required=False, validate=validate.Length(min=0, max=100))
    sort = fields.String(required=False,
                         validate=validate.OneOf(["question", "answer", "created_date", "modified_date"]))
    order_by = fields.String(required=False, validate=validate.OneOf(["asc", "desc"]))


class QuestionValidation(Schema):
    """
    Marshmallow Schema
    Target: validate parameters of faq question
    """
    question = fields.String(required=True, validate=validate.Length(min=1, max=200))
    answer = fields.String(required=True, validate=validate.Length(min=1, max=2000))


class QuestionSchema(Schema):
    """
    Marshmallow Schema

    """
    id = fields.String()
    question = fields.String()
    answer = fields.String()
    created_date = fields.Number()
    modified_date = fields.Number()


class CreateCartElement(Schema):
    """
    Marshmallow Schema
    Author: LyChan
    Target: Use for create Cart element
    """
    product_id = fields.String(required=True, validate=validate.Length(min=1, max=50))
    quantity = fields.Number(required=True)
    is_buy_later = fields.Boolean()
    is_buy_now = fields.Boolean()


class CreateCartValidation(Schema):
    """
    Marshmallow Schema
    Author: LyChan
    Target: Use for create Cart
    """
    carts = fields.List(Nested(CreateCartElement()), required=True)


class ProductSchema(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    """

    id = fields.String()
    original_code = fields.String()
    name = fields.String()
    other_name = fields.String()
    code = fields.String()
    price = fields.Integer()
    final_price = fields.Float()
    description = fields.String()
    specification = fields.String()
    user_manual = fields.String()
    warranty = fields.String()
    avatar_url = fields.String()
    other_images_url = fields.String()
    inventory_number = fields.Integer()
    sold = fields.Integer()
    views = fields.Integer()
    discount_percent = fields.Float()
    discount_value = fields.Integer()
    is_active = fields.Boolean()
    is_top = fields.Boolean()
    product_unit = fields.Integer()
    is_sale = fields.Boolean()
    is_new = fields.Boolean()
    is_best_selling = fields.Boolean()
    link_seo = fields.String()
    images = fields.List(fields.String())

    created_date = fields.Number()
    modified_date = fields.Number()

    category = Nested(CategorySchema(exclude=["children", "specifications", "models"]))
    original_manufacturer = Nested(CategorySchema(exclude=["children", "specifications", "models"]))
    manufacturer = Nested(CategorySchema(exclude=["children", "specifications", "models"]))
    models = fields.List(Nested(ModelSchema(exclude=["children"])))
    specifications = fields.List(Nested(SpecificationSchema()))
    similar_products = fields.List(fields.Nested(lambda: ProductSchema(exclude=["similar_products"])))


"""
===================================
Handle manage product admin
"""


class CategoryValidate(Schema):
    """
    Marshmallow Schema

    """
    id = fields.String()


class ModelValidate(Schema):
    """
        Marshmallow Schema
        Author: Phongnv
        Target:
    """

    id = fields.String()


class ProductSpecificationValidate(Schema):
    """
    Author: phonnv
    Marshmallow Schema
    """
    specification_id = fields.String()
    value = fields.Float()


class ProductValidate(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    """

    original_code = fields.String(validate=validate.Length(min=1, max=20))
    name = fields.String(validate=validate.Length(min=1, max=100))
    other_name = fields.String()
    code = fields.String(validate=validate.Length(min=1, max=30))
    price = fields.Integer()
    description = fields.String(validate=validate.Length(min=0, max=6000))
    specification = fields.String(validate=validate.Length(min=0, max=6000))
    user_manual = fields.String(validate=validate.Length(min=0, max=6000))
    warranty = fields.String(validate=validate.Length(min=0, max=6000))
    avatar_url = fields.String()
    other_images_url = fields.String()
    inventory_number = fields.Integer()
    discount_percent = fields.Float()
    discount_value = fields.Integer()
    is_active = fields.Boolean()
    is_top = fields.Boolean()

    product_category = Nested(CategoryValidate())
    product_original_manufacturer = Nested(CategoryValidate())
    product_manufacturer = Nested(CategoryValidate())
    product_models = fields.List(Nested(ModelValidate()))
    product_specifications = fields.List(Nested(ProductSpecificationValidate()), required=True)


class CartSchema(Schema):
    """
    Marshmallow Schema
    Author: LyChan
    Target: Use for Cart
    """
    id = fields.String()
    user_id = fields.String()
    product_id = fields.String(required=True, validate=validate.Length(min=1, max=50))
    quantity = fields.Number(required=True)
    is_buy_later = fields.Boolean()
    created_date = fields.Number()
    modified_date = fields.Number()
    product = Nested(ProductSchema(exclude=["category"]))


class OrderDeliveryAddressSchema(Schema):
    """
    Marshmallow Schema
    Author: LyChan
    Target: Use for Order Delivery Info
    """

    id = fields.String()
    type = fields.Integer()
    full_name = fields.String()
    phone = fields.String()
    address = fields.String()
    city = fields.String()
    district = fields.String()
    town = fields.String()
    note = fields.String()


class OrderProductSchema(Schema):
    id = fields.String()
    quantity = fields.Integer()
    price = fields.Float()
    original_price = fields.Float()
    product = Nested(ProductSchema(only=["id", "name", "final_price", "price", "manufacturer", "avatar_url"]))


class DeliveryAddressSchema(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    """
    id = fields.String()
    type = fields.Integer()
    full_name = fields.String()
    phone = fields.String()
    address = fields.String()
    city = fields.String()
    district = fields.String()
    town = fields.String()
    note = fields.String()
    is_default = fields.Integer()
    created_date = fields.Integer()
    modified_date = fields.Integer()


class DeliveryAddressValidate(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    """
    type = fields.Integer(required=True, validate=validate.OneOf([1, 2, 3]))
    full_name = fields.String(required=True,
                              validate=[validate.Length(min=1, max=50), validate.Regexp(REGEX_FULLNAME_VIETNAMESE)])
    phone = fields.String(required=True,
                          validate=[validate.Length(min=1, max=20), validate.Regexp(REGEX_PHONE_NUMBER)])
    address = fields.String(required=True,
                            validate=[validate.Length(min=1, max=50), validate.Regexp(REGEX_ADDRESS_VIETNAMESE)])
    city = fields.String(required=True, validate=[validate.Length(min=1, max=250)])
    district = fields.String(required=True, validate=[validate.Length(min=1, max=250)])
    town = fields.String(required=True, validate=[validate.Length(min=1, max=250)])
    note = fields.String()
    is_default = fields.Boolean()


class OrderDeliveryAddressValidate(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    """
    type = fields.Integer(required=False)
    full_name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    phone = fields.String(required=True, validate=validate.Length(min=1, max=20))
    address = fields.String(required=False)
    city = fields.String(required=False)
    district = fields.String(required=False)
    town = fields.String(required=False)
    note = fields.String(required=False, validate=validate.Length(min=0, max=200))


class StoreAddressSchema(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    """
    id = fields.String()
    store_name = fields.String()
    address = fields.String()
    phone = fields.String()
    created_date = fields.Integer()
    modified_date = fields.Integer()


class OrderStoreAddressSchema(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    """
    id = fields.String()
    store_name = fields.String()
    address = fields.String()
    phone = fields.String()


class OrderStoreAddressValidate(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    """
    store_name = fields.String(required=False)
    address = fields.String(required=False)
    phone = fields.String(required=False)


class PaymentInfoSchema(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    """
    id = fields.String()
    bank_name = fields.String()
    account_name = fields.String()
    bank_number = fields.String()
    payment_content = fields.String()
    momo_phone = fields.String()
    created_date = fields.Integer()
    modified_date = fields.Integer()


class PaymentInfoValidate(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    """
    bank_name = fields.String()
    account_name = fields.String()
    bank_number = fields.String()
    payment_content = fields.String()
    momo_phone = fields.String()


class OrderPaymentInfoSchema(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    """
    id = fields.String()
    bank_name = fields.String()
    account_name = fields.String()
    bank_number = fields.String()
    payment_content = fields.String()
    momo_phone = fields.String()


class OrderPaymentInfoValidate(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    """
    bank_name = fields.String(required=False)
    account_name = fields.String(required=False)
    bank_number = fields.String(required=False)
    payment_content = fields.String(required=False)
    momo_phone = fields.String(required=False)


class VatInvoicesSchema(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    """
    id = fields.String()
    company_name = fields.String()
    tax_identification_number = fields.String()
    company_address = fields.String()
    is_default = fields.Integer()
    created_date = fields.Integer()
    modified_date = fields.Integer()


class OrderVatInvoicesSchema(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    """
    id = fields.String()
    company_name = fields.String()
    tax_identification_number = fields.String()
    company_address = fields.String()
    is_default = fields.Integer()
    created_date = fields.Integer()
    modified_date = fields.Integer()


class VatInvoiceValidate(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    """
    company_name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    tax_identification_number = fields.String(required=True, validate=[validate.Length(min=1, max=20),
                                                                       validate.Regexp(RE_ONLY_NUMBER_AND_DASH)])
    company_address = fields.String(required=True, validate=validate.Length(min=1, max=100))
    is_default = fields.Boolean()


class OrderVatInvoicesValidate(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    """
    company_name = fields.String(required=False)
    tax_identification_number = fields.String(required=False)
    company_address = fields.String(required=False)


class FilterOrderValidate(Schema):
    """
    Marshmallow Schema
    Author: LyChan
    Target: Use for admin to search order
    """
    page = fields.Integer()
    page_size = fields.Integer()
    order_code = fields.String(validate=[validate.Length(min=0, max=50)])
    status = fields.Integer()
    customer = fields.String(validate=[validate.Length(min=0, max=50)])
    user_id = fields.String(validate=[validate.Length(min=0, max=50)])
    from_date = fields.Integer()
    to_date = fields.Integer()
    sort = fields.String(validate=validate.OneOf(
        choices=["order_code", "full_name", "phone", "final_total_price", "created_date", "expected_delivery",
                 "delivered_date", "status"],
        error="Sort must be one of these columns [order_code, full_name, phone, final_total_price, created_date, "
              "expected_delivery, delivered_date or status]"))
    order_by = fields.String(validate=validate.OneOf(choices=["asc", "desc"],
                                                     error="Order by must be one of [asc, desc]"))


class OrderUpdateTypeValidate(Schema):
    """
    Marshmallow Schema
    Author: LyChan
    Target: Use for admin to update order type
    """
    type = fields.String(validate=validate.OneOf(choices=["status", "shipper_info"],
                                                 error="type must be one of [status, shipper_info]"))



class OrderSchema(Schema):
    """
    Marshmallow Schema
    Author: LyChan
    Target: Use for admin to manage orders
    """
    id = fields.String()
    user_id = fields.String()
    status = fields.Integer()
    order_code = fields.String()
    cancel_reason = fields.String()
    cancel_by = fields.Integer()
    payment_method = fields.Integer()
    note = fields.String()
    vat_invoice = fields.Boolean()
    delivery_method = fields.Integer()
    create_status = fields.Integer()
    expected_delivery = fields.Number()
    delivered_date = fields.Number()
    shipping_unit = fields.String()
    handover_shipping = fields.Number()
    shipper_name = fields.String()
    shipper_phone = fields.String()
    total_price = fields.Number()
    shipping_fee = fields.Number()
    discount_value = fields.Number()
    tax = fields.Number()
    final_total_price = fields.Number()
    is_active = fields.Boolean()
    created_date = fields.Number()
    modified_date = fields.Number()
    discount_id = fields.String()

    order_products = fields.List(fields.Nested(OrderProductSchema))
    order_delivery_address = Nested(OrderDeliveryAddressSchema())
    order_store_address = Nested(OrderStoreAddressSchema())
    order_payment_info = Nested(OrderPaymentInfoSchema())
    order_vat_invoice = Nested(OrderVatInvoicesSchema())


class CartUpdateValidation(Schema):
    """
    Marshmallow Schema
    Author: LyChan
    Target: Use for Cart
    """
    quantity = fields.Number()
    is_buy_later = fields.Boolean()


class HistorySeenSchema(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    """
    id = fields.String()
    product = Nested(ProductSchema())
    created_date = fields.Integer()
    modified_date = fields.Integer()


class SearchKeywordHistorySchema(Schema):
    """
    Marshmallow Schema
    Author: Cong Sy Nguyen
    """
    id = fields.String(required=True, validate=validate.Length(min=0, max=50))
    keyword = fields.String(validate=validate.Length(min=0, max=100))
    user_id = fields.String(required=True, validate=validate.Length(min=0, max=50))
    created_date = fields.Integer()
    modified_date = fields.Integer()


class KeywordMappingSchema(Schema):
    """
    Author: Cong Sy Nguyen
    Marshmallow Schema
    """
    id = fields.String(required=True, validate=validate.Length(min=0, max=50))
    object_id = fields.String(validate=validate.Length(min=0, max=50))
    object_name = fields.String(validate=validate.Length(min=0, max=255))
    name = fields.String(validate=validate.Length(min=0, max=255))
    keyword = fields.String()
    created_date = fields.Integer()
    modified_date = fields.Integer()


class SearchProductParamsValidator(Schema):
    """
    Author: Cong Sy Nguyen
    Marshmallow Schema for Product query params validator
    """
    page = fields.Integer(required=False)
    page_size = fields.Integer(required=False)
    specifications = fields.List(fields.Nested(SpecificationValidator))
    sort_by = fields.String(required=False, validate=validate.OneOf(["price", "time", "sales"]))
    order = fields.String(required=False, validate=validate.OneOf(["asc", "desc"]))
    category_ids = fields.List(fields.String(required=False, validate=validate.Length(min=0, max=50)))
    manufacturer_ids = fields.List(fields.String(required=False, validate=validate.Length(min=0, max=50)))
    model_ids = fields.List(fields.String(required=False, validate=validate.Length(min=0, max=50)))
    keyword = fields.String(required=False, validate=validate.Length(min=0, max=100))
    is_top = fields.Boolean(required=False)


class AdminSearchProductParamsValidator(Schema):
    """
    Author: Phongnv
    Marshmallow Schema for Product query params validator
    """
    page = fields.Integer(required=False)
    page_size = fields.Integer(required=False)
    specifications = fields.List(fields.Nested(SpecificationValidator))
    sort_by = fields.String(required=False, validate=validate.OneOf(
        choices=["original_code", "name", "other_name", "code", "price", "final_price", "created_date", "category_name",
                 "manufacturer_name", "inventory_number", "is_active"]))
    order = fields.String(required=False, validate=validate.OneOf(["asc", "desc"]))
    category_ids = fields.List(fields.String(required=False, validate=validate.Length(min=0, max=50)))
    manufacturer_ids = fields.List(fields.String(required=False, validate=validate.Length(min=0, max=50)))
    model_ids = fields.List(fields.String(required=False, validate=validate.Length(min=0, max=50)))
    keyword = fields.String(required=False, validate=validate.Length(min=0, max=100))
    is_top = fields.Boolean(required=False)


class CategoryMappingProduct(Schema):
    """
    Author: Cong Sy Nguyen
    Marshmallow Schema
    """
    id = fields.String()
    name = fields.String()


class ManufacturerMappingProduct(Schema):
    """
    Author: Cong Sy Nguyen
    Marshmallow Schema
    """
    id = fields.String()
    name = fields.String()


class ProductModelMappingProduct(Schema):
    """
    Author: Cong Sy Nguyen
    Marshmallow Schema
    """
    id = fields.String()
    name = fields.String()


class ProductSpecificationSchema(Schema):
    """
    Author: Cong Sy Nguyen
    Marshmallow Schema
    """
    id = fields.String()
    specification_id = fields.String()
    product_id = fields.String()
    value = fields.Float()

    specification = Nested(SpecificationSchema)


class OrderProductValidate(Schema):
    product_id = fields.String(required=False)
    name = fields.String(required=False)
    quantity = fields.Integer(required=False)


class OrderValidate(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    Target: Use for Create Order
    """
    payment_method = fields.Integer(required=False)
    note = fields.String(required=False)
    delivery_method = fields.Integer(required=True)
    create_status = fields.Integer(required=False)
    discount_code = fields.String(required=False, validate=validate.Length(min=1, max=50))

    order_products = fields.List(fields.Nested(OrderProductValidate))
    order_store_address = fields.Nested(OrderStoreAddressValidate)
    order_delivery_address = fields.Nested(OrderDeliveryAddressValidate)
    order_payment_info = fields.Nested(OrderPaymentInfoValidate)
    order_vat_invoice = fields.Nested(OrderVatInvoicesValidate)


class CancelOrderValidate(Schema):
    """
    Marshmallow Schema
    Author: LucDV
    Target: Use for Cancel Order
    """
    cancel_reason = fields.String(required=False, validate=validate.Length(min=0, max=500))


class DiscountSchema(Schema):
    """
    Marshmallow Schema
    Author: LyChan
    Target: Use for discount
    """
    id = fields.String()
    code = fields.String()
    description = fields.String()
    discount_type = fields.Integer()
    number_use = fields.Integer()
    number_user_used = fields.Integer()
    quantity = fields.Integer()
    discount_percent = fields.Float()
    discount_value = fields.Integer()
    minimum_total = fields.Integer()
    start_discount_date = fields.Integer()
    end_discount_date = fields.Integer()
    start_oder_date = fields.Integer()
    end_order_date = fields.Integer()
    address_conditions = fields.Integer()

    created_date = fields.Integer()
    modified_date = fields.Integer()


class DiscountValidate(Schema):
    """
    Marshmallow Schema
    Author: LyChan
    Target: Use for validate discount
    """
    code = fields.String(required=True, validate=validate.Length(min=0, max=50))
    description = fields.String(required=True, validate=validate.Length(min=0, max=200))
    discount_type = fields.Integer(required=True)
    number_use = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    discount_percent = fields.Float(required=False, validate=validate.Range(min=0, max=100))
    discount_value = fields.Integer()
    minimum_total = fields.Integer()
    start_discount_date = fields.Integer(required=True)
    end_discount_date = fields.Integer(required=True)
    start_oder_date = fields.Integer()
    end_order_date = fields.Integer()
    address_conditions = fields.Integer()


class PermissionSchema(Schema):
    """
    Marshmallow Schema
    Author: LyChan
    Target: Use for permission
    """
    id = fields.String()
    name = fields.String()
    resource = fields.String()


class RolePermissionSchema(Schema):
    """
    Marshmallow Schema
    Author: LyChan
    Target: Use for permission
    """
    id = fields.String()
    role_id = fields.String()
    permission_id = fields.String()


class DocumentCategorySchema(Schema):
    """
    Marshmallow Schema
    Target: Use for DocumentCategory
    """
    id = fields.String()
    name = fields.String()
    description = fields.String()
    link_seo = fields.String()
    created_date = fields.Integer()
    modified_date = fields.Integer()


class DocumentCategoryValidation(Schema):
    """
    Marshmallow Schema
    Target: Use for DocumentCategoryValidation
    """
    name = fields.String(required=True, validate=[validate.Length(min=1, max=50)])
    description = fields.String(validate=[validate.Length(min=0, max=500)])


class DocumentValidation(Schema):
    """
    Marshmallow Schema
    Target: Use for Document
    """
    name = fields.String(required=True, validate=[validate.Length(min=1, max=100)])
    file_url = fields.String(validate=[validate.Length(min=0, max=250)])
    file_size = fields.Float(required=True, validate=validate.Range(min=0, max=50))
    document_category_id = fields.String(required=True, validate=[validate.Length(min=1, max=50)])


class DocumentSchema(Schema):
    """
    Marshmallow Schema
    Target: Use for Document
    """
    id = fields.String()
    name = fields.String()
    file_url = fields.String()
    file_size = fields.Float()
    link_seo = fields.String()
    document_category_id = fields.String()
    created_date = fields.Integer()
    modified_date = fields.Integer()
    category = fields.Nested(DocumentCategorySchema)


class FilterDocumentCategoryValidate(Schema):
    """
    Marshmallow Schema
    Author: LyChan
    Target: Use for admin to search DocumentCategory
    """
    page = fields.Integer()
    page_size = fields.Integer()
    name = fields.String(validate=[validate.Length(min=0, max=50)])
    sort = fields.String(validate=validate.OneOf(
        choices=["name", "description", "created_date"],
        error="Sort must be one of these columns [name, description, created_date]"))
    order_by = fields.String(validate=validate.OneOf(choices=["asc", "desc"],
                                                     error="Order by must be one of [asc, desc]"))


class FilterDocumentValidate(Schema):
    """
    Marshmallow Schema
    Author: LyChan
    Target: Use for admin to search Document
    """
    page = fields.Integer()
    page_size = fields.Integer()
    name = fields.String(validate=[validate.Length(min=0, max=50)])
    document_category_id = fields.String(validate=[validate.Length(min=0, max=50)])
    from_date = fields.Integer()
    to_date = fields.Integer()
    sort = fields.String(validate=validate.OneOf(
        choices=["name", "category_name", "created_date"],
        error="Sort must be one of these columns [title, category_name, created_date]"))
    order_by = fields.String(validate=validate.OneOf(choices=["asc", "desc"],
                                                     error="Order by must be one of [asc, desc]"))


class FilterDocumentCustomerValidate(Schema):
    """
    Marshmallow Schema
    Author: LyChan
    Target: Use for customer to filter documents
    """
    page = fields.Integer()
    page_size = fields.Integer()
    name = fields.String(validate=[validate.Length(min=0, max=100)])
    document_categories_id = fields.List(fields.String(validate=[validate.Length(min=0, max=50)]))


class RoleSchema(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    Target: Use for permission
    """
    id = fields.String()
    key = fields.String()
    name = fields.String()
    description = fields.String()
    is_show = fields.Boolean()
    type = fields.Integer()


class RoleValidate(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    Target: Use for permission
    """
    id = fields.String()


class GroupValidate(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    Target: Use for permission
    """

    key = fields.String(required=False)
    name = fields.String(required=False)
    description = fields.String(required=False)
    password_admin = fields.String(required=False)
    roles = fields.List(fields.Nested(RoleValidate), required=False)
    method = fields.Integer(required=True)


class GroupDeleteValidate(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    Target: Use for permission
    """

    password_admin = fields.String(required=True)


class GroupSchema(Schema):
    """
    Marshmallow Schema
    Author: phongnv
    Target: Use for permission
    """
    id = fields.String()
    key = fields.String(required=False)
    name = fields.String(required=False)
    description = fields.String(required=False)

    roles = fields.List(fields.Nested(RoleSchema))


class SearchGroupParamsValidator(Schema):
    """
    Author: Phongnv
    Marshmallow Schema for Product query params validator
    """
    page = fields.Integer(required=False)
    page_size = fields.Integer(required=False)
    specifications = fields.List(fields.Nested(SpecificationValidator))
    sort_by = fields.String(required=False, validate=validate.OneOf(choices=["name", "description", "created_date"]))
    order = fields.String(required=False, validate=validate.OneOf(["asc", "desc"]))
    keyword = fields.String(required=False, validate=validate.Length(min=0, max=100))


class SearchUserAdminParamsValidator(Schema):
    """
    Author: Phongnv
    Marshmallow Schema for Product query params validator
    """
    page = fields.Integer(required=False)
    page_size = fields.Integer(required=False)
    specifications = fields.List(fields.Nested(SpecificationValidator))
    type = fields.Integer(required=False)
    sort_by = fields.String(required=False, validate=validate.OneOf(
        choices=["full_name", "created_date", "phone", "email", "gender", "birthday", "order_number", "is_active",
                 "group"]))
    order = fields.String(required=False, validate=validate.OneOf(["asc", "desc"]))
    keyword = fields.String(required=False, validate=validate.Length(min=0, max=100))
    date_of_birth_begin = fields.String(required=False, validate=validate.Length(min=0, max=100))
    date_of_birth_end = fields.String(required=False, validate=validate.Length(min=0, max=100))
    # gender = fields.Boolean(required=False)
    gender = fields.Integer(required=False)


class UserValidation(Schema):
    """
    Validator
    :param
        full_name: string, required
        permission_group_id: string, required
        is_active: bool, option
    Ex:
    {
        "email": "superadmin@mayno.vn",
        "password": "admin",
        "is_admin": true
    }
    """
    full_name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    permission_group_id = fields.String(required=True, validate=validate.Length(max=255))
    is_active = fields.Boolean(required=True)


class AdminProfileValidation(Schema):
    """
    Validator
    :param
        full_name: string, required
        avatar_url: string
    Ex:
    {
        "full_name": "Nguyễn Văn A",
        "avatar_url": "#"
    }
    """
    full_name = fields.String(required=False, validate=validate.Length(min=1, max=50))
    avatar_url = fields.String(validate=validate.Length(max=250))


class SendQuestionValidation(Schema):
    """
    Author: LucDV
    Marshmallow Schema for Product query params validator
    """
    email = fields.String(required=True, validate=[validate.Length(min=3, max=50), validate.Regexp(REGEX_EMAIL)])
    full_name = fields.String(required=True,
                              validate=[validate.Length(min=1, max=50), validate.Regexp(REGEX_FULLNAME_VIETNAMESE)])
    title = fields.String(required=True, validate=validate.Length(min=1, max=100))
    content = fields.String(required=True, validate=validate.Length(min=1, max=500))


class EmailTemplateSchema(Schema):
    """
    Marshmallow Schema
    Target: Use for Email template
    """
    id = fields.String()
    title = fields.String()
    subject = fields.String()
    body = fields.String()
    description = fields.String()
    template_code = fields.String()
    object = fields.String()


class StatisticRevenueSchema(Schema):
    """
    Marshmallow Schema
    Target: Use for Email template
    """
    amount_order = fields.Integer()
    final_total_price = fields.Float()
    created_date = fields.Integer()
    time = fields.String()


class StatisticProductSchema(Schema):
    """
    Marshmallow Schema
    Target: Use for Email template
    """
    code = fields.String()
    name = fields.String()
    average_price = fields.Float()
    sum_quantity = fields.Integer()
    sum_final_total_price = fields.Float()
    product_id = fields.String()


class VerifyPasswordValidation(Schema):
    """
    Validator
    :param
        current_password: string, required
    Ex:
    {
        "current_password": "12345678A?a"
    }
    """
    current_password = fields.String(required=True,
                                     validate=[validate.Length(min=1, max=16), validate.Regexp(REGEX_VALID_PASSWORD)])

from django.contrib import admin

from .models import ContactSupport, ContractorAgreement, ContractorData, CooperationOffer


@admin.register(ContractorData)
class ContractorDataAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "is_active",
        "company_name",
        "phone_number",
        "requisites",
    ]


@admin.register(ContactSupport)
class ContactSupportAdmin(admin.ModelAdmin):
    list_display = ["user_account", "user_question", "created"]


@admin.register(CooperationOffer)
class CooperationOfferAdmin(admin.ModelAdmin):
    list_display = ["name", "telephone", "created"]


@admin.register(ContractorAgreement)
class ContractorAgreementAdmin(admin.ModelAdmin):
    list_display = ["user_account", "created_date"]

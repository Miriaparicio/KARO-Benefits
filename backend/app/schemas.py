from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from app.models import BenefitCategoryEnum, TaxTypeEnum, RoleEnum, AssignmentStatusEnum

# ==================== Auth Schemas ====================

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)

# ==================== Employee Schemas ====================

class EmployeeCreate(BaseModel):
    vorname: str = Field(..., min_length=1)
    nachname: str = Field(..., min_length=1)
    personalnummer: str = Field(..., min_length=1, max_length=20)
    email: EmailStr
    abteilung: Optional[str] = None
    eintrittsdatum: Optional[datetime] = None

class EmployeeUpdate(BaseModel):
    vorname: Optional[str] = None
    nachname: Optional[str] = None
    email: Optional[EmailStr] = None
    abteilung: Optional[str] = None
    eintrittsdatum: Optional[datetime] = None

class EmployeeResponse(BaseModel):
    id: int
    vorname: str
    nachname: str
    personalnummer: str
    email: str
    abteilung: Optional[str]
    eintrittsdatum: Optional[datetime]
    aktiv: bool
    erstellt_am: datetime

    class Config:
        from_attributes = True

# ==================== Benefit Type Schemas ====================

class BenefitTypeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=30)
    kategorie: BenefitCategoryEnum
    beschreibung: Optional[str] = None
    betrag_max_monat: Optional[float] = None
    steuerart: TaxTypeEnum
    rechtsgrundlage: Optional[str] = None
    datev_lohnart_nr: Optional[str] = Field(None, regex=r"^\d{4}$")

class BenefitTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=30)
    kategorie: Optional[BenefitCategoryEnum] = None
    beschreibung: Optional[str] = None
    betrag_max_monat: Optional[float] = None
    steuerart: Optional[TaxTypeEnum] = None
    rechtsgrundlage: Optional[str] = None

class BenefitTypeLohnartUpdate(BaseModel):
    datev_lohnart_nr: Optional[str] = Field(None, regex=r"^\d{4}$")

class BenefitTypeResponse(BaseModel):
    id: int
    name: str
    kategorie: BenefitCategoryEnum
    beschreibung: Optional[str]
    betrag_max_monat: Optional[float]
    steuerart: TaxTypeEnum
    rechtsgrundlage: Optional[str]
    datev_lohnart_nr: Optional[str]
    datev_lohnart_nr_aktualisiert_am: Optional[datetime]
    aktiv: bool
    erstellt_am: datetime

    class Config:
        from_attributes = True

# ==================== Assignment Schemas ====================

class BenefitAssignmentCreate(BaseModel):
    employee_id: int
    benefit_type_id: int
    monat: str = Field(..., regex=r"^\d{4}-\d{2}$")
    betrag: float = Field(..., gt=0)
    kommentar: Optional[str] = None

class BenefitAssignmentUpdate(BaseModel):
    betrag: Optional[float] = Field(None, gt=0)
    kommentar: Optional[str] = None

class BenefitAssignmentResponse(BaseModel):
    id: int
    employee_id: int
    benefit_type_id: int
    monat: str
    betrag: float
    status: AssignmentStatusEnum
    kommentar: Optional[str]
    erstellt_am: datetime
    geaendert_am: Optional[datetime]

    class Config:
        from_attributes = True

class BenefitAssignmentWithDetails(BenefitAssignmentResponse):
    employee: EmployeeResponse
    benefit_type: BenefitTypeResponse

# ==================== Dashboard Schemas ====================

class DashboardStats(BaseModel):
    total_employees: int
    active_employees: int
    benefit_types_count: int
    assignments_this_month: int
    total_cost_this_month: float
    missing_lohnart_count: int

# ==================== Export Schemas ====================

class ExportPreviewRow(BaseModel):
    personalnummer: str
    monat: str
    lohnart_nr: Optional[str]
    betrag_formatted: str
    name: str
    warning: Optional[str]

class ExportPreviewResponse(BaseModel):
    rows: List[ExportPreviewRow]
    total_rows: int
    warning_rows: int

# ==================== User Schemas ====================

class CurrentUser(BaseModel):
    id: int
    email: str
    rolle: RoleEnum

    class Config:
        from_attributes = True

#!/usr/bin/env python
"""
Initialize database with demo data.
Run once: python seed.py
"""

from app.database import SessionLocal, engine
from app.models import Base, User, Employee, BenefitType, BenefitCategoryEnum, TaxTypeEnum, RoleEnum
from app.auth import get_password_hash
from datetime import datetime

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Create admin user
admin = User(
    email="admin@karo-gmbh.de",
    hashed_password=get_password_hash("KaroAdmin2026!"),
    rolle=RoleEnum.ADMIN,
    aktiv=True,
    erstellt_am=datetime.utcnow()
)
db.add(admin)
db.commit()

# Create demo employee
employee = Employee(
    vorname="Max",
    nachname="Mustermann",
    personalnummer="0001",
    email="max.mustermann@karo-gmbh.de",
    abteilung="IT",
    eintrittsdatum=datetime(2023, 1, 15),
    aktiv=True
)
db.add(employee)
db.commit()

# Create employee user
emp_user = User(
    email="max.mustermann@karo-gmbh.de",
    hashed_password=get_password_hash("MitarbeiterPass123!"),
    rolle=RoleEnum.MITARBEITER,
    employee_id=employee.id,
    aktiv=True
)
db.add(emp_user)
db.commit()

# Create benefit types (DATEV payroll numbers initially NULL - to be added by admin)
benefits = [
    BenefitType(
        name="Sachbezug Gutscheinkarte",
        kategorie=BenefitCategoryEnum.SACHBEZUG,
        beschreibung="Essens-/Warengutscheine bis Freigrenze",
        betrag_max_monat=50.0,
        steuerart=TaxTypeEnum.STEUERFREI,
        rechtsgrundlage="§ 8 Abs. 2 EStG",
        datev_lohnart_nr=None,  # To be filled by admin
        aktiv=True
    ),
    BenefitType(
        name="Essenszuschuss",
        kategorie=BenefitCategoryEnum.VERPFLEGUNG,
        beschreibung="Arbeitgeberzuschuss zur Verpflegung",
        betrag_max_monat=115.05,
        steuerart=TaxTypeEnum.STEUERFREI,
        rechtsgrundlage="SvEV 2026",
        datev_lohnart_nr=None,
        aktiv=True
    ),
    BenefitType(
        name="Jobticket/Deutschlandticket",
        kategorie=BenefitCategoryEnum.MOBILITAET,
        beschreibung="ÖPNV-Fahrkarte oder Deutschlandticket",
        betrag_max_monat=63.0,
        steuerart=TaxTypeEnum.STEUERFREI,
        rechtsgrundlage="§ 3 Nr. 15 EStG",
        datev_lohnart_nr=None,
        aktiv=True
    ),
    BenefitType(
        name="Gesundheitsförderung",
        kategorie=BenefitCategoryEnum.GESUNDHEIT,
        beschreibung="Betriebliche Gesundheitsförderung (Fitness, etc.)",
        betrag_max_monat=50.0,
        steuerart=TaxTypeEnum.STEUERFREI,
        rechtsgrundlage="§ 3 Nr. 34 EStG",
        datev_lohnart_nr=None,
        aktiv=True
    ),
    BenefitType(
        name="Aufmerksamkeit (pers. Anlass)",
        kategorie=BenefitCategoryEnum.SONSTIGES,
        beschreibung="Geschenke zu persönlichen Anlässen",
        betrag_max_monat=60.0,
        steuerart=TaxTypeEnum.GELDWERTER_VORTEIL,
        rechtsgrundlage="R 19.6 LStR",
        datev_lohnart_nr=None,
        aktiv=True
    ),
]

for benefit in benefits:
    db.add(benefit)

db.commit()

print("✅ Database initialized successfully!")
print("\nDemo credentials:")
print("  Admin:      admin@karo-gmbh.de / KaroAdmin2026!")
print("  Employee:   max.mustermann@karo-gmbh.de / MitarbeiterPass123!")
print("\nNext steps:")
print("  1. Start backend: uvicorn app.main:app --reload")
print("  2. Go to http://localhost:8000/docs for API documentation")
print("  3. Add DATEV payroll numbers in Admin → Benefit Types")

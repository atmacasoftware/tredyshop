from import_export import resources
from product.models import *

class BrandResource(resources.ModelResource):
    class Meta:
        model = Brand

class ColorResource(resources.ModelResource):
    class Meta:
        model = Color

class SizeResource(resources.ModelResource):
    class Meta:
        model = Size

class FabricTypeResource(resources.ModelResource):
    class Meta:
        model = FabricType

class HeightResource(resources.ModelResource):
    class Meta:
        model = Height

class PatternResource(resources.ModelResource):
    class Meta:
        model = Pattern


class ArmTypeResource(resources.ModelResource):
    class Meta:
        model = ArmType

class CollerTypeResource(resources.ModelResource):
    class Meta:
        model = CollerType

class WeavingTypeResource(resources.ModelResource):
    class Meta:
        model = WeavingType


class MaterialTypeResource(resources.ModelResource):
    class Meta:
        model = MaterialType


class EnvironmentTypeResource(resources.ModelResource):
    class Meta:
        model = EnvironmentType


class WaistResource(resources.ModelResource):
    class Meta:
        model = Waist


class LegTypeResource(resources.ModelResource):
    class Meta:
        model = LegType


class PocketResource(resources.ModelResource):
    class Meta:
        model = Pocket

class HeelTypeResource(resources.ModelResource):
    class Meta:
        model = HeelType


class HeelSizeResource(resources.ModelResource):
    class Meta:
        model = HeelSize

class SexResource(resources.ModelResource):
    class Meta:
        model = Sex


class KadinUstBedenResource(resources.ModelResource):
    class Meta:
        model = KadinUstBedenTablosu


class KadinUstBuyukBedenResource(resources.ModelResource):
    class Meta:
        model = KadinUstBuyukBedenTablosu

class KadinAltBedenResource(resources.ModelResource):
    class Meta:
        model = KadinAltBedenTablosu

class KadinAltBuyukBedenResource(resources.ModelResource):
    class Meta:
        model = KadinAltBuyukBedenTablosu

class KadinJeanBedenResource(resources.ModelResource):
    class Meta:
        model = KadinJeanBedenTablosu

class TabletModelResource(resources.ModelResource):
    class Meta:
        model = TabletModel

class TableCaseTypeResource(resources.ModelResource):
    class Meta:
        model = TableCaseType

class SleepModeResource(resources.ModelResource):
    class Meta:
        model = SleepMode

class BagPatternResource(resources.ModelResource):
    class Meta:
        model = BagPattern

class BijuteriThemeResource(resources.ModelResource):
    class Meta:
        model = BijuteriTheme

class DesenResource(resources.ModelResource):
    class Meta:
        model = Desen

class PaketIcerigiResource(resources.ModelResource):
    class Meta:
        model = PaketIcerigi

class KoleksiyonResource(resources.ModelResource):
    class Meta:
        model = Koleksiyon

class DokumaTipiResource(resources.ModelResource):
    class Meta:
        model = DokumaTipi

class OzellikResource(resources.ModelResource):
    class Meta:
        model = Ozellik

class UrunDetayResource(resources.ModelResource):
    class Meta:
        model = UrunDetay

class PersonaResource(resources.ModelResource):
    class Meta:
        model = Persona

class SiluetResource(resources.ModelResource):
    class Meta:
        model = Siluet

class AltSiluetResource(resources.ModelResource):
    class Meta:
        model = AltSiluet

class UstSiluetResource(resources.ModelResource):
    class Meta:
        model = UstSiluet

class PadDetayResource(resources.ModelResource):
    class Meta:
        model = PadDetay

class ProductVariantResource(resources.ModelResource):
    class Meta:
        model = ProductVariant
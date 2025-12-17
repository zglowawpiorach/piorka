from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page

class Product(models.Model):
    # Choices for fields
    PRZEZNACZENIE_CHOICES = [
        ('kolczyki_para', 'Do ucha - kolczyki (para)'),
        ('kolczyki_asymetria', 'Do ucha - kolczyki (asymetria)'),
        ('kolczyki_single', 'Do ucha - kolczyki (single)'),
        ('kolczyki_komplet', 'Do ucha - kolczyki (komplet z wisiorkiem)'),
        ('zausznice', 'Zausznice'),
        ('na_szyje', 'Na szyję'),
        ('na_reke', 'Na rękę'),
        ('do_wlosow', 'Do włosów'),
        ('inne', 'Inne'),
    ]

    DLA_KOGO_CHOICES = [
        ('dla_niej', 'Dla niej'),
        ('dla_niego', 'Dla niego'),
        ('unisex', 'Unisex'),
    ]

    DLUGOSC_KATEGORIA_CHOICES = [
        ('krotkie', 'Krótkie'),
        ('srednie', 'Średnie'),
        ('dlugie', 'Długie'),
        ('bardzo_dlugie', 'Bardzo długie'),
    ]

    KOLOR_PIOR_CHOICES = [
        ('bezowy', 'Beżowy'),
        ('bialy', 'Biały'),
        ('brazowy', 'Brązowy'),
        ('czerwony', 'Czerwony'),
        ('czarny', 'Czarny'),
        ('granatowy', 'Granatowy'),
        ('niebieski', 'Niebieski'),
        ('rozowy', 'Różowy'),
        ('szary', 'Szary'),
        ('turkusowy', 'Turkusowy'),
        ('wzor', 'Wzór'),
        ('zolty', 'Żółty'),
        ('wielokolorowe', 'Wielokolorowe'),
    ]

    GATUNEK_PTAKOW_CHOICES = [
        ('bazant', 'Bażant'),
        ('emu', 'Emu'),
        ('gawron', 'Gawron'),
        ('indyk', 'Indyk'),
        ('kura_kogut', 'Kura lub kogut'),
        ('papuga', 'Papuga'),
        ('paw', 'Paw'),
        ('perlica', 'Perlica'),
        ('inny', 'Inny'),
    ]

    KOLOR_METALOWYCH_CHOICES = [
        ('zloty', 'Złoty'),
        ('srebrny', 'Srebrny'),
        ('mieszany', 'Mieszany'),
        ('inny', 'Inny'),
    ]

    RODZAJ_ZAPIECIA_CHOICES = [
        ('bigiel_otwarty', 'Bigiel otwarty'),
        ('bigiel_zamkniety', 'Bigiel zamknięty'),
        ('sztyft', 'Sztyft'),
        ('kolko', 'Kółko'),
        ('klips', 'Klips'),
        ('zausznik', 'Zausznik'),
        ('inny', 'Inny'),
        ('nie_dotyczy', 'Nie dotyczy'),
    ]

    PYTANIE_O_PRZEDMIOT_CHOICES = [
        ('zamiana_zapiecia', 'Zamiana zapięcia'),
        ('inna_przerobka', 'Inna przeróbka'),
        ('szybsza_wysylka', 'Szybsza wysyłka'),
        ('zamowienie_indywidualne', 'Zamówienie indywidualne'),
        ('odbior_osobisty', 'Odbiór osobisty'),
        ('inne', 'Inne'),
    ]

    # Basic fields
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_price_id = models.CharField(max_length=255, blank=True, help_text="Stripe Price ID for checkout")
    stripe_product_id = models.CharField(max_length=255, blank=True, help_text="Stripe Product ID")
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False, verbose_name="Wyróżnij na stronie głównej")
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # New fields
    nr_w_katalogu_zdjec = models.CharField(max_length=255, blank=True, verbose_name="Nr w katalogu zdjęć")
    przeznaczenie_ogolne = models.CharField(max_length=50, choices=PRZEZNACZENIE_CHOICES, blank=True, verbose_name="Przeznaczenie ogólne")
    tytul = models.CharField(max_length=255, blank=True, verbose_name="Tytuł")
    opis = models.TextField(blank=True, verbose_name="Opis")
    dla_kogo = models.CharField(max_length=20, choices=DLA_KOGO_CHOICES, blank=True, verbose_name="Dla kogo")
    cena = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Cena")
    dlugosc_kategoria = models.CharField(max_length=20, choices=DLUGOSC_KATEGORIA_CHOICES, blank=True, verbose_name="Długość kategoria")
    dlugosc_w_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Długość w cm")
    kolor_pior = models.CharField(max_length=30, choices=KOLOR_PIOR_CHOICES, blank=True, verbose_name="Kolor piór w przewadze")
    gatunek_ptakow = models.CharField(max_length=30, choices=GATUNEK_PTAKOW_CHOICES, blank=True, verbose_name="Pióra zgubiły (gatunek)")
    kolor_elementow_metalowych = models.CharField(max_length=20, choices=KOLOR_METALOWYCH_CHOICES, blank=True, verbose_name="Kolor elementów metalowych")
    rodzaj_zapiecia = models.CharField(max_length=30, choices=RODZAJ_ZAPIECIA_CHOICES, blank=True, verbose_name="Rodzaj zapięcia")
    pytanie_o_przedmiot = models.CharField(max_length=50, choices=PYTANIE_O_PRZEDMIOT_CHOICES, blank=True, verbose_name="Pytanie o przedmiot")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('slug'),
            FieldPanel('active'),
            FieldPanel('featured'),
        ], heading="Basic Info"),
        MultiFieldPanel([
            FieldPanel('nr_w_katalogu_zdjec'),
            FieldPanel('tytul'),
            FieldPanel('opis'),
            FieldPanel('description'),
        ], heading="Opisy"),
        MultiFieldPanel([
            FieldPanel('price'),
            FieldPanel('cena'),
        ], heading="Ceny"),
        FieldPanel('image'),
        MultiFieldPanel([
            FieldPanel('przeznaczenie_ogolne'),
            FieldPanel('dla_kogo'),
        ], heading="Przeznaczenie"),
        MultiFieldPanel([
            FieldPanel('dlugosc_kategoria'),
            FieldPanel('dlugosc_w_cm'),
        ], heading="Wymiary"),
        MultiFieldPanel([
            FieldPanel('kolor_pior'),
            FieldPanel('gatunek_ptakow'),
        ], heading="Pióra"),
        MultiFieldPanel([
            FieldPanel('kolor_elementow_metalowych'),
            FieldPanel('rodzaj_zapiecia'),
        ], heading="Elementy metalowe i zapięcia"),
        FieldPanel('pytanie_o_przedmiot'),
        MultiFieldPanel([
            FieldPanel('stripe_product_id'),
            FieldPanel('stripe_price_id'),
        ], heading="Stripe Integration"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class HomePage(Page):
    pass

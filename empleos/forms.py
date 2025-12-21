from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import OfertaLaboral, Candidato, Valoracion, Suscriptor, PerfilEmpresa, ReporteOferta, Pregunta

PALABRAS_PROHIBIDAS = ['estafa', 'dinero facil', 'sexo', 'xxx', 'idiota', 'tonto', 'basura']
def validar_texto_limpio(texto):
    if texto:
        texto_bajo = texto.lower()
        for palabra in PALABRAS_PROHIBIDAS:
            if palabra in texto_bajo: raise ValidationError(f"Palabra prohibida: '{palabra}'")

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['pregunta']
        widgets = {'pregunta': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Haz una pregunta profesional al reclutador...'})}

class ContactoForm(forms.Form):
    nombre = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    asunto = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mensaje = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))

class SuscriptorForm(forms.ModelForm):
    class Meta: model = Suscriptor; fields = ['email']; widgets = {'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu correo...'})}

class ValoracionForm(forms.ModelForm):
    class Meta: model = Valoracion; fields = ['estrellas', 'comentario']; widgets = {'estrellas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}), 'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})}

class PerfilEmpresaForm(forms.ModelForm):
    class Meta:
        model = PerfilEmpresa
        fields = ['nombre', 'logo', 'banner', 'sitio_web', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'banner': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields: self.fields[field].required = False

class ReporteForm(forms.ModelForm):
    class Meta:
        model = ReporteOferta; fields = ['motivo', 'detalle']
        widgets = {'motivo': forms.Select(attrs={'class': 'form-select'}), 'detalle': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})}

class NuevaOfertaForm(forms.ModelForm):
    aceptar_terminos = forms.BooleanField(required=False)
    wsp_activo = forms.BooleanField(required=False, label="Permitir contacto por WhatsApp", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    captcha = forms.IntegerField(required=False, label="3 + 4 = ?", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = OfertaLaboral
        # AQUÍ ESTÁ EL CAMPO WSP_ACTIVO QUE DABA ERROR
        fields = ['titulo', 'empresa', 'tipo', 'duracion', 'modalidad', 'region', 'experiencia', 'sueldo', 'fecha_cierre', 'telefono', 'wsp_activo', 'email_contacto', 'etiquetas', 'descripcion', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Vendedor'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'experiencia': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'duracion': forms.TextInput(attrs={'class': 'form-control'}),
            'modalidad': forms.Select(attrs={'class': 'form-control'}),
            'sueldo': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_cierre': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 ...'}),
            'email_contacto': forms.EmailInput(attrs={'class': 'form-control'}),
            'etiquetas': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields: self.fields[field].required = False
        if not self.instance.pk: self.fields['fecha_cierre'].initial = (timezone.now() + timedelta(days=30)).date()

    def clean_telefono(self):
        tel = self.cleaned_data.get('telefono')
        if not tel: return None
        tel = tel.replace(" ", "").replace("-", "").replace("+", "")
        if not tel.isdigit(): raise forms.ValidationError("Solo números")
        return tel

    def clean_imagen(self):
        img = self.cleaned_data.get('imagen')
        if img and img.size > 2*1024*1024: raise ValidationError("Máx 2MB")
        return img

    def clean_captcha(self):
        val = self.cleaned_data.get('captcha')
        if val is None: return 7 
        if val != 7: raise forms.ValidationError("Error robot")
        return 7

class NuevoCandidatoForm(forms.ModelForm):
    aceptar_terminos = forms.BooleanField(required=False)
    captcha = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Candidato
        # AQUÍ ESTÁ EL CAMPO VIDEO QUE DABA ERROR
        fields = ['nombre', 'titular', 'rubro', 'foto', 'video', 'region', 'experiencia', 'pretension_renta', 'disponibilidad', 'telefono', 'email', 'linkedin', 'cv', 'presentacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'titular': forms.TextInput(attrs={'class': 'form-control'}),
            'rubro': forms.Select(attrs={'class': 'form-select'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'experiencia': forms.Select(attrs={'class': 'form-select'}),
            'pretension_renta': forms.NumberInput(attrs={'class': 'form-control'}),
            'disponibilidad': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'presentacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cv': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields: self.fields[field].required = False

    def clean_telefono(self):
        tel = self.cleaned_data.get('telefono')
        if not tel: return None
        return tel

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo Electrónico", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.cl'}))
    first_name = forms.CharField(required=True, label="Nombre", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Juan'}))
    last_name = forms.CharField(required=True, label="Apellido", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pérez'}))
    captcha = forms.IntegerField(required=True, label="Seguridad: ¿Cuánto es 5 + 5?", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Respuesta numéríca'}))
    aceptar_legales = forms.BooleanField(required=True, label="Acepto los Términos y Política de Privacidad bajo la legislación chilena.")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario único'})}
        help_texts = {'username': None}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists(): raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean_captcha(self):
        val = self.cleaned_data.get('captcha')
        if val != 10: raise forms.ValidationError("Error matemático. ¿Eres un robot?")
        return val
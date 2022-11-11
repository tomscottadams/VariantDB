from django import forms
from .models import *
from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML

class SearchForm(forms.Form):
    chr_choices = [
    ('',''),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10','10'),
    ('11','11'),
    ('12','12'),
    ('13','13'),
    ('14','14'),
    ('15','15'),
    ('16','16'),
    ('17','17'),
    ('18','18'),
    ('19','19'),
    ('20','20'),
    ('21','21'),
    ('22','22'),
    ('x', 'x'),
    ('y', 'y')]

    var_class_choices = [
        ('',''),
        ('SNP','SNP'),
        ('deletion','deletion'),
        ('insertion','insertion')
    ]

    clin_sig_choices = [
        ('',''),
        ('pathogenic','pathogenic'),
        ('likely pathogenic','likely pathogenic'),
        ('uncertain significance','uncertain significance'),
        ('likely benign','likely benign'),
        ('benign','benign'),
        ('not provided','not provided')       
    ]
    
    
    start = forms.CharField(required=False, max_length = 50)
    end = forms.CharField(required=False, max_length = 50)
    chr = forms.ChoiceField(required=False, widget=forms.Select, choices=chr_choices)
    variant_class = forms.ChoiceField(required=False, widget=forms.Select, choices=var_class_choices)
    clinical_significance = forms.ChoiceField(required=False, widget=forms.Select, choices=clin_sig_choices)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        
        
        self.helper = FormHelper()
        self.helper.form_id = 'manual-upload-form'
        self.helper.label_class = 'col-lg-2' # Set from Crispy Form Template 
        self.helper.field_class = 'col-lg-10' # Set from Crispy Form Template 
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'search', css_class='btn-success'))
        
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            HTML('<br><h5>Search</h5>'),
            Field('chr'),
            Field('start', placeholder="Enter start position" ),
            Field('end', placeholder="Enter end position" ),
            Field('variant_class'),
            Field('clinical_significance')
            
        )  



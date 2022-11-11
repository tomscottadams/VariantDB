from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
from .forms import *
#from .serializers import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

import pymongo
import pandas as pd
import numpy as np



# Create your views here.
def index(request):
    return HttpResponse("<h1>Hello and welcome to my first <u>Django App</u> project!</h1>")

client = pymongo.MongoClient('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.0')

#Define Db Name
dbname = client['Advanced_IT']

#Define Collection
collection = dbname['variants']


def home(request):
    return render(request, 'variantdb/home.html')

def search(request):
    context = {'search_form': SearchForm()}
    path_page = 'variantdb/search.html'
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            try:
                chr = search_form.cleaned_data.get('chr')
            except:
                chr = False
            try:
                start = int(search_form.cleaned_data.get('start'))
            except:
                start = False
            try:
                end = int(search_form.cleaned_data.get('end'))
            except:
                end = False
            try:
                var = search_form.cleaned_data.get('variant_class')
            except:
                var = False
            try:
                clin_sig = search_form.cleaned_data.get('clinical_significance')
            except:
                clin_sig = False

            print(clin_sig)
            

            query = {}



            if chr:

                query['mappings.seq_region_name'] = chr
        
                
            if start:
                query['mappings.start'] = {'$gte':start}
        

            if end:
                query['mappings.end'] = {'$lte':end}
        
            
            if var:
                query['var_class'] = var

            
            if clin_sig:
                query['clinical_significance'] = {'$in':[clin_sig]}

            
            response_json = collection.find({'$and':[query]})

            allrecords = collection.find()

            context['max_count'] = len(list(allrecords))
            
            context['count'] = len(list(response_json))
            
            response_json = collection.find({'$and':[query]})
            
            if context['count'] > 0:
                context['chr_result'] = list(response_json)


                df = pd.DataFrame(context['chr_result'])
        

                context['intron_variant_count'] = df[df.most_severe_consequence == 'intron_variant'].shape[0]
                context['missense_variant_count'] = df[df.most_severe_consequence == 'missense_variant'].shape[0]
                context['synonymous_variant_count'] = df[df.most_severe_consequence == 'synonymous_variant'].shape[0]
                context['frameshift_variant_count'] = df[df.most_severe_consequence == 'frameshift_variant'].shape[0]
                context['five_prime_UTR_variant_count'] = df[df.most_severe_consequence == '5_prime_UTR_variant'].shape[0]
                context['inframe_deletion_count'] = df[df.most_severe_consequence == 'inframe_deletion'].shape[0]
                context['non_coding_transcript_exon_variant_count'] = df[df.most_severe_consequence == 'non_coding_transcript_exon_variant'].shape[0]
                context['stop_gained_count'] = df[df.most_severe_consequence == 'stop_gained'].shape[0]
                context['downstream_gene_variant_count'] = df[df.most_severe_consequence == 'downstream_gene_variant'].shape[0]
                context['three_prime_UTR_variant_count'] = df[df.most_severe_consequence == '3_prime_UTR_variant'].shape[0]
                context['splice_region_variant_count'] = df[df.most_severe_consequence == 'splice_region_variant'].shape[0]
                context['splice_donor_variant_count'] = df[df.most_severe_consequence == 'splice_donor_variant'].shape[0]
            else:
                context['zero_records'] = 'Zero records found'
    
    return render(request, path_page, context)

def results(request):
    return render(request, 'variantdb/results.html')



#for r in all:
#    print(r)
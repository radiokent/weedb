import re
from django.shortcuts import render, redirect, HttpResponseRedirect
from .tables import SearchForm
from annotation.models import GeneExp, Gene, GeneNeighbor, Transcript, FunctionAnn
from django.db.models import Q
from collections import defaultdict


GENE_PATTERN = re.compile(r'TraesCS(\w+)1G(\w+)')
GENE_NUM_UP = 100
TPM_LOWER = 0.0001

def iwgsc1to2(gene_id):
    """
    TraesCS3D01G355600 -> TraesCS3D02G355600
    """
    if GENE_PATTERN.match(gene_id):
        id_1, id_2 = GENE_PATTERN.match(gene_id).groups()
        return 'TraesCS{id_1}2G{id_2}'.format(**locals())
    else:
        return gene_id


def search_view(request, warning=''):
    form = SearchForm()
    return render(request, 'search/index.html', {
        'form': form,
        'warning': warning,
    })


def exp2chart(gene_obj, color=None):
    tissues = []
    exp_values = []
    for gene_i in gene_obj:
        gene_i_id = gene_i.gene_id
        gene_i_exp = dict()
        gene_i_exp['name'] = gene_i_id
        gene_i_exp['data'] = []
        if color is not None:
            gene_i_exp['color'] = color
        for exp_i in gene_i.gene_exp.all():
            tissue = exp_i.tissue
            tpm = exp_i.tpm
            if tpm < TPM_LOWER:
                tpm = TPM_LOWER
            if tissue not in tissues:
                tissues.append(tissue)
            gene_i_exp['data'].append(float(tpm))
        exp_values.append(gene_i_exp)
    return tissues, exp_values


def result_view(request, db):
    form = SearchForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        gene_list = [iwgsc1to2(each.strip()) for each in cd['genes'].split('\n')]
        if len(gene_list) > GENE_NUM_UP:
            return search_view(request, warning=f'Most {GENE_NUM_UP} query genes are allowed!')
        request.session['gene_list'] = gene_list
    elif 'gene_list' in request.session:
        pass
    else:
        return search_view(request, warning='Your should submit a gene list first!')
    if db == 'exp':
        gene_exp = GeneExp.objects.filter(
            gene_id__gene_id__in=request.session['gene_list'])
        gene_obj = Gene.objects.filter(
            gene_id__in=request.session['gene_list'])
        tissues, exp_values = exp2chart(gene_obj)

        return render(
            request, 'search/results.html', {
                'gene_exp': gene_exp,
                'tissues': tissues,
                'exp_values': exp_values,
            })
    elif db == 'nb':
        neighbor_inf = GeneNeighbor.objects.filter(
            Q(lncRNA_gene__gene_id__in=request.session['gene_list'])
            | Q(partnerRNA_gene__gene_id__in=request.session['gene_list']))
        if neighbor_inf.exists():
            mrna_genes = {nb.partnerRNA_gene for nb in neighbor_inf}
            lncrna_genes = {nb.lncRNA_gene for nb in neighbor_inf}
            tissues, mrna_exp = exp2chart(mrna_genes, color='#058DC7')
            _, lncrna_exp = exp2chart(lncrna_genes, color='red')
            exp_values = mrna_exp + lncrna_exp
        else:
            tissues = []
            exp_values = []
        query_id = ' '.join(request.session['gene_list'])
        return render(
            request, 'search/neighbor.html', {
                'neighbor_inf': neighbor_inf,
                'gene_name': query_id,
                'tissues': tissues,
                'exp_values': exp_values,
            })
    elif db == 'ann':
        ann_inf = FunctionAnn.objects.filter(
            gene_id__gene_id__in=request.session['gene_list'])
        return render(request, 'search/annotation.html', {
            'ann_inf': ann_inf,
        })
    else:
        return search_view(request, warning='URL not found!')


def gene_detail(request, gene_id):
    tr_inf = Gene.objects.get(gene_id=gene_id)
    return render(request, 'search/gene_detail.html', {'tr_inf': tr_inf})


def tr_detail(request, tr_id):
    tr_inf = Transcript.objects.get(tr_id=tr_id)
    return render(request, 'search/tr_detail.html', {'tr_inf': tr_inf})


def single_gene_exp_view(request, gene_id):
    gene_exp = GeneExp.objects.filter(gene_id__gene_id=gene_id)
    gene_obj = Gene.objects.filter(gene_id=gene_id)
    tissues, exp_values = exp2chart(gene_obj)
    return render(
        request, 'search/results.html', {
            'gene_exp': gene_exp,
            'tissues': tissues,
            'exp_values': exp_values,
        })


def search_neighbor(request, query_id):
    neighbor_inf = GeneNeighbor.objects.filter(
        Q(lncRNA_gene__gene_id=query_id) | Q(partnerRNA_gene__gene_id=query_id)
        | Q(lncRNA_transcript__tr_id=query_id)
        | Q(partnerRNA_transcript__tr_id=query_id))
    if neighbor_inf.exists():
        mrna_genes = {nb.partnerRNA_gene for nb in neighbor_inf}
        lncrna_genes = {nb.lncRNA_gene for nb in neighbor_inf}
        tissues, mrna_exp = exp2chart(mrna_genes, color='#058DC7')
        _, lncrna_exp = exp2chart(lncrna_genes, color='red')
        exp_values = mrna_exp + lncrna_exp
    return render(
        request, 'search/neighbor.html', {
            'neighbor_inf': neighbor_inf,
            'gene_name': query_id,
            'tissues': tissues,
            'exp_values': exp_values,
        })

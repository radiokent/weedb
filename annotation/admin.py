from django.contrib import admin
from .models import FunctionAnn, Gene, GeneExp, GeneNeighbor, GeneType
from .models import Transcript, GeneLoc


@admin.register(FunctionAnn)
class FunctionAnnAdmin(admin.ModelAdmin):
    list_display = (
        'gene_id',
        'tr_id',
        'blast_hit',
        'description',
        'pfam',
        'interpro',
        'go',
    )


@admin.register(Gene)
class Genedmin(admin.ModelAdmin):
    list_display = ('gene_id', )


@admin.register(GeneExp)
class GeneExpAdmin(admin.ModelAdmin):
    list_display = (
        'gene_id',
        'tpm',
        'tissue',
    )


@admin.register(GeneNeighbor)
class GeneNeighborAdmin(admin.ModelAdmin):
    list_display = (
        'lncRNA_gene',
        'lncRNA_transcript',
        'partnerRNA_gene',
        'partnerRNA_transcript',
        'direction',
        'generic_type',
        'distance',
        'subtype',
        'location',
        'isBest',
    )


@admin.register(GeneType)
class GeneTypeAdmin(admin.ModelAdmin):
    list_display = (
        'gene_id',
        'gene_biotype',
    )


@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    list_display = (
        'tr_id',
        'gene_id',
    )


@admin.register(GeneLoc)
class GeneLocAdmin(admin.ModelAdmin):
    list_display = (
        'tr_id',
        'gene_id',
        'feature',
        'start',
        'end',
        'strand',
    )
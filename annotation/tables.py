import django_tables2 as tables
from django_tables2.utils import A
from .models import FunctionAnn, GeneExp, GeneNeighbor, FunctionAnn


class ExpTable(tables.Table):

    description = tables.Column(accessor='gene_id.gene_description',
                                empty_values=(),
                                verbose_name='Description')
    gene_id = tables.LinkColumn('search:gene_detail',
                                args=[A('gene_id.gene_id')])
    gene_neighbor = tables.LinkColumn(
        'search:search_neighbor',
        args=[A('gene_id.gene_id')],
        text=lambda record: record.gene_id.gene_neighbor_num(),
        verbose_name='Gene-Neighbours',
    )

    class Meta:
        model = GeneExp
        template_name = "django_tables2/semantic.html"
        fields = (
            'gene_id',
            'tissue',
            'tpm',
            'description',
            'gene_neighbor',
        )


class GeneNeighborTable(tables.Table):

    lncRNA_gene = tables.LinkColumn('search:gene_detail',
                                    args=[A('lncRNA_gene.gene_id')])
    partnerRNA_gene = tables.LinkColumn('search:gene_detail',
                                        args=[A('partnerRNA_gene.gene_id')])
    lncRNA_transcript = tables.LinkColumn('search:tr_detail',
                                          args=[A('lncRNA_transcript.tr_id')])
    partnerRNA_transcript = tables.LinkColumn(
        'search:tr_detail', args=[A('partnerRNA_transcript.tr_id')])

    class Meta:
        model = GeneNeighbor
        template_name = "django_tables2/semantic.html"

        fields = (
            'lncRNA_gene',
            'lncRNA_transcript',
            'partnerRNA_gene',
            'partnerRNA_transcript',
            'direction',
            'generic_type',
            'distance',
            'subtype',
            'location',
            'pcc',
            'pcc_pva',
        )


class GeneAnnTable(tables.Table):

    gene_id = tables.LinkColumn('search:gene_detail',
                                args=[A('gene_id.gene_id')])
    tr_id = tables.LinkColumn('search:tr_detail', args=[A('tr_id.tr_id')])

    class Meta:
        model = FunctionAnn
        template_name = "django_tables2/semantic.html"

        fields = (
            'gene_id',
            'tr_id',
            'is_repr',
            'blast_hit',
            'description',
            'pfam',
            'interpro',
            'go',
        )

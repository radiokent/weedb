from django.db import models
from django.urls import reverse
from django.db.models import Min, Max

STRAND_NAME = {
    '+': 'forward',
    '-': 'reverse',
    '.': 'unknown',
}


class Gene(models.Model):
    gene_id = models.CharField(max_length=50)

    class Meta:
        ordering = ('gene_id', )

    def __str__(self):
        return self.gene_id

    def get_absolute_url(self):
        return reverse('search:gene_detail', args=[self.gene_id])

    def gene_description(self):
        try:
            gene_des = self.function.get(is_repr=1).description
        except FunctionAnn.DoesNotExist:
            gene_des = 'Unknown'
        return gene_des

    def gene_go(self):
        try:
            gene_des = '\n'.join(self.function.get(is_repr=1).go.split(';'))
        except FunctionAnn.DoesNotExist:
            gene_des = 'Unknown'
        return gene_des

    def gene_pfam(self):
        try:
            gene_des = '\n'.join(self.function.get(is_repr=1).pfam.split('; '))
        except FunctionAnn.DoesNotExist:
            gene_des = 'Unknown'
        return gene_des

    def gene_interpro(self):
        try:
            gene_des = '\n'.join(
                self.function.get(is_repr=1).interpro.split('; '))
        except FunctionAnn.DoesNotExist:
            gene_des = 'Unknown'
        return gene_des

    def gene_neighbor_obj(self):
        gene_neighbor_set = set()
        if self.gene_neighbor.exists():
            for nb_i in self.gene_neighbor.all():
                gene_neighbor_set.add(nb_i.partnerRNA_gene)
        elif self.neighbor_gene.exists():
            for nb_i in self.neighbor_gene.all():
                gene_neighbor_set.add(nb_i.lncRNA_gene)
        else:
            pass
        return gene_neighbor_set

    def gene_neighbor_num(self):
        return len(self.gene_neighbor_obj())

    def gene_start(self):
        return self.position.all().order_by('start').first().start

    def gene_end(self):
        return self.position.all().order_by('-end').first().end

    def gene_strand(self):
        return STRAND_NAME.get(self.position.first().strand)

    def gene_chrom(self):
        return self.position.first().seqname.replace('chr', 'Chromosome ')

    def exp_inf(self):
        min_tpm = self.gene_exp.all().aggregate(Min('tpm'))['tpm__min']
        max_tpm = self.gene_exp.all().aggregate(Max('tpm'))['tpm__max']
        min_tpm_items = self.gene_exp.filter(tpm=min_tpm)
        max_tpm_items = self.gene_exp.filter(tpm=max_tpm)

        def tissue_msg(tissue_items):
            add_inf = ''
            if len(tissue_items) > 5:
                remain_tissues = len(tissue_items) - 5
                tissue_items = tissue_items[:5]
                add_inf = f' and {remain_tissues} other tissues'
            msg = ','.join([item.tissue for item in tissue_items]) + add_inf
            return msg

        min_tpm_tissue = tissue_msg(min_tpm_items)
        max_tpm_tissue = tissue_msg(max_tpm_items)
        return {
            'max_tpm': round(max_tpm, 3),
            'max_tissue': max_tpm_tissue,
            'min_tpm': round(min_tpm, 3),
            'min_tissue': min_tpm_tissue,
        }

    def repr_tr(self):
        max_cds = 0
        max_exon = 0
        rep_tr = None
        rep_tr_bak = None
        for tr in self.transcript.all():
            tr_cds_inf = tr.cds_inf()
            tr_exon_inf = tr.exon_inf()
            if tr_cds_inf:
                if tr_cds_inf['c_len'] > max_cds:
                    max_cds = tr_cds_inf['c_len']
                    rep_tr = tr
            else:
                if tr_exon_inf['e_len'] > max_exon:
                    max_exon = tr_exon_inf['e_len']
                    rep_tr_bak = tr
        if rep_tr is not None:
            return rep_tr
        else:
            return rep_tr_bak


class Transcript(models.Model):
    tr_id = models.CharField(max_length=20, verbose_name='Transcript-ID')
    gene_id = models.ForeignKey(Gene,
                                on_delete=models.CASCADE,
                                related_name='transcript',
                                verbose_name='Gene-ID')

    class Meta:
        ordering = ('tr_id', )

    def __str__(self):
        return self.tr_id

    def get_absolute_url(self):
        return reverse('search:tr_detail', args=[self.tr_id])

    def tr_des(self):
        ann = 'Unknown'
        ann_inf = self.function.first()
        if ann_inf is not None:
            ann = self.function.first().description
        return ann

    def tr_go(self):
        ann = 'Unknown'
        ann_inf = self.function.first()
        if ann_inf is not None:
            ann = '\n'.join(self.function.first().go.strip().split(';'))
        return ann

    def tr_pfam(self):
        ann = 'Unknown'
        ann_inf = self.function.first()
        if ann_inf is not None:
            ann = '\n'.join(self.function.first().pfam.strip().split('; '))
        return ann

    def tr_interpro(self):
        ann = 'Unknown'
        ann_inf = self.function.first()
        if ann_inf is not None:
            ann = '\n'.join(self.function.first().interpro.strip().split('; '))
        return ann

    def tr_neighbor_obj(self):
        tr_neighbor_set = set()
        if self.tr_neighbor.exists():
            for nb_i in self.tr_neighbor.all():
                tr_neighbor_set.add(nb_i.partnerRNA_gene)
        elif self.neighbor_tr.exists():
            for nb_i in self.neighbor_tr.all():
                tr_neighbor_set.add(nb_i.lncRNA_gene)
        else:
            pass
        return tr_neighbor_set

    def tr_start(self):
        return self.position.all().order_by('start').first().start

    def tr_end(self):
        return self.position.all().order_by('-end').first().end

    def tr_strand(self):
        return STRAND_NAME.get(self.position.first().strand)

    def tr_chrom(self):
        return self.position.first().seqname.replace('chr', 'Chromosome ')

    def exon_inf(self):
        exon_items = self.position.filter(feature='exon')
        if exon_items.exists():
            exon_len = sum([exon.end - exon.start + 1 for exon in exon_items])
            return {'e_count': exon_items.count(), 'e_len': exon_len}
        else:
            return {}

    def cds_inf(self):
        cds_items = self.position.filter(feature='CDS')
        if cds_items.exists():
            cds_len = sum([exon.end - exon.start + 1 for exon in cds_items])
            return {'c_count': cds_items.count(), 'c_len': cds_len}
        else:
            return {}

    def exon_fa(self):
        return self.sequence.filter(feature='exon')

    def cds_fa(self):
        return self.sequence.filter(feature='CDS')


class FunctionAnn(models.Model):
    tr_id = models.ForeignKey(Transcript,
                              on_delete=models.CASCADE,
                              verbose_name='Transcript-ID',
                              related_name='function')
    gene_id = models.ForeignKey(Gene,
                                on_delete=models.CASCADE,
                                related_name='function',
                                verbose_name='Gene-ID')
    is_repr = models.IntegerField(verbose_name='Is-Repr')
    blast_hit = models.CharField(max_length=50,
                                 verbose_name='Blast-Hit-Accession')
    description = models.CharField(max_length=250,
                                   verbose_name='Human-Readable-Description')
    pfam = models.CharField(max_length=250,
                            verbose_name='Pfam-IDs-(Description)')
    interpro = models.CharField(max_length=250,
                                verbose_name='Interpro-IDs-(Description)')
    go = models.CharField(max_length=250,
                          verbose_name='GO-IDs-(Description)-via-Interpro')

    class Meta:
        ordering = ('tr_id', )

    def __str__(self):
        return self.tr_id.tr_id


class GeneExp(models.Model):
    gene_id = models.ForeignKey(Gene,
                                on_delete=models.CASCADE,
                                related_name='gene_exp',
                                verbose_name='Gene-ID')
    tpm = models.DecimalField(max_digits=10, decimal_places=3)
    tissue = models.CharField(max_length=20)

    class Meta:
        ordering = ('gene_id', )

    def __str__(self):
        return str(self.gene_id)


class GeneNeighbor(models.Model):
    isBest = models.IntegerField()
    lncRNA_gene = models.ForeignKey(Gene,
                                    on_delete=models.CASCADE,
                                    related_name='gene_neighbor')
    lncRNA_transcript = models.ForeignKey(Transcript,
                                          on_delete=models.CASCADE,
                                          related_name='tr_neighbor')
    partnerRNA_gene = models.ForeignKey(Gene,
                                        on_delete=models.CASCADE,
                                        related_name='neighbor_gene')
    partnerRNA_transcript = models.ForeignKey(Transcript,
                                              on_delete=models.CASCADE,
                                              related_name='neighbor_tr')
    direction = models.CharField(max_length=9)
    generic_type = models.CharField(max_length=10)
    distance = models.IntegerField()
    subtype = models.CharField(max_length=11)
    location = models.CharField(max_length=10)
    pcc = models.DecimalField(max_digits=4, decimal_places=3, verbose_name='PCC')
    pcc_pva = models.DecimalField(max_digits=4, decimal_places=3, verbose_name='PCC-Pvalue')

    class Meta:
        ordering = (
            'partnerRNA_transcript',
            'distance',
        )

    def __str__(self):
        return f'{self.lncRNA_gene}-{self.partnerRNA_gene}'


class GeneType(models.Model):
    gene_id = models.ForeignKey(Gene,
                                on_delete=models.CASCADE,
                                related_name='gene_type')
    gene_biotype = models.CharField(max_length=28)

    class Meta:
        ordering = ('gene_id', )

    def __str__(self):
        return f'{self.gene_id}-{self.gene_biotype}'


class GeneLoc(models.Model):
    gene_id = models.ForeignKey(Gene,
                                on_delete=models.CASCADE,
                                related_name='position')
    tr_id = models.ForeignKey(Transcript,
                              on_delete=models.CASCADE,
                              related_name='position')
    feature = models.CharField(max_length=4, db_index=True)
    seqname = models.CharField(max_length=5, db_index=True)
    start = models.IntegerField()
    end = models.IntegerField()
    strand = models.CharField(max_length=1)

    class Meta:
        ordering = (
            'tr_id',
            'feature',
            'start',
            'end',
        )

    def __str__(self):
        return f'{self.tr_id} {self.feature} {self.seqname}:{self.start}-{self.end}'


class GeneSeq(models.Model):
    tr_id = models.ForeignKey(Transcript,
                              on_delete=models.CASCADE,
                              related_name='sequence')
    feature = models.CharField(max_length=4, db_index=True)
    seq_index = models.IntegerField()
    seq = models.CharField(max_length=60)

    class Meta:
        ordering = (
            'tr_id',
            'feature',
            'seq_index',
        )

    def __str__(self):
        return f'{self.tr_id}-{self.feature}-seq{self.seq_index}'

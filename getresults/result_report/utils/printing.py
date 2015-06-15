#import sys
import os
import subprocess
import cStringIO as StringIO
import ho
import pisa as pisa
from math import ceil, trunc
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from lis.subject.lab_patient.models import Patient
from lis.specimen.lab_result.models import Result
from lis.specimen.lab_result_item.models import ResultItem


def batch_print_result_as_pdf(**kwargs):

    subject_identifier = kwargs.get('subject_identifier')
    if subject_identifier:
        oPatient = get_object_or_404(Patient, subject_identifier=subject_identifier)
        patient_results = Result.objects.filter(order__aliquot__receive__patient=oPatient)
        template = 'result_report_pdf.html'
        for result in patient_results:
            file_name = print_result_as_pdf(result.result_identifier, template)
            command = "lp {0}".format(file_name)
            try:
                p = subprocess.Popen(command, shell=True)
                pid, sts = os.waitpid(p.pid, 0)
            except subprocess.CalledProcessError, e:
                print "Error", e.returncode
                print e.output
    return


def print_result_as_pdf(result_identifier, template):
    section_name = 'result'
    search_name = 'result'
    num_items_last_page = 18
    num_items_first_page = 13
    num_items_per_page = 23
    total_page_number = 1
    result = get_object_or_404(Result, result_identifier=result_identifier)
    items = ResultItem.objects.filter(result=result)
    num_items = items.count()
    if num_items > num_items_first_page:
        if (num_items - num_items_first_page) > num_items_last_page:
            num_items_other = num_items - num_items_first_page - num_items_last_page
            total_page_number += trunc(ceil(num_items_other / float(num_items_per_page)))
        else:
            total_page_number = 2
    if result:
        file_name = "/home/pmotshegwa/sources/printed_results/%s.pdf" % (result_identifier)
        file = open(file_name, "wb")
        result = get_object_or_404(Result, result_identifier=result_identifier)
        items = ResultItem.objects.filter(result=result)
        total_page_number = trunc(ceil(items.count() / float(18)))
        payload = {
            'pagesize': 'A4',
            'total_page_number': total_page_number,
            'result': result,
            'receive': result.order.aliquot.receive,
            'order': result.order,
            'getresults_aliquot': result.order.aliquot,
            'result_items': items,
            'section_name': section_name,
            'result_include_file': "detail.html",
            'receiving_include_file': "receiving.html",
            'orders_include_file': "orders.html",
            'result_items_include_file': "result_items.html",
            'top_result_include_file': "result_include.html",
        }
        file_data = render_to_string(template, payload,)
        myfile = StringIO.StringIO()
        pdf = pisa.CreatePDF(file_data, myfile)
        if pdf.err:
            print "*** {0} ERRORS OCCURED".format(pdf.err)
        else:
            # Write pdf file to disk
            file.write(myfile.getvalue())
            file.close()
            return file_name
    return


def print_barcode_label(**kwargs):
    """
    usage:
    e.g >>> print_barcode_label (result_identifier='xxxxxxx-xx',num_labels=3,printer='mochudi_id01'"""
    tmp_folder = "/home/pmotshegwa/sources/barcode"
    scp_server = "roche@bartender.bhp.org.bw"
    #Name of the folder where to dump the *.tmp file
    barcoder_printer_folder = kwargs.get('printer')
    result_identifier = kwargs.get('result_identifier')
    num_of_labels = kwargs.get('num_labels')
    remote_folder = "/cygdrive/c/dmis/commander/%s/" % (barcoder_printer_folder)
    if num_of_labels is None or num_of_labels < 1:
        num_of_labels = 1
    result = get_object_or_404(Result, result_identifier=result_identifier)
    file_name = "%s/%s.tmp" % (tmp_folder, result_identifier)
    file = open(file_name, "wb")
    file.write("protocolnumber,pat_id,label,seq,seq_total\n")
    for n in range(0, num_of_labels):
        data = "Result,%s,BHPLAB,1,35\n" % (result_identifier)
        file.write(data)
    command = "scp %s %s:%s" % (file_name, scp_server, remote_folder)
    #print command
    file.close()
    os.system(command)
    return

from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
import json
import models


def export(request, sheet_name):
    deploy_sheet = querySheetByName(sheet_name)
    if not deploy_sheet:
        return {}
    result = dict()
    deploy_vars = list(deploy_sheet.variables_set.all())
    result["Variables"] = dict()
    for var in deploy_vars:
        result["Variables"][var.Attr_Name] = var.Attr_Value
    
    deploy_inst = list(deploy_sheet.instances_set.all())
    result["Instances"] = dict()
    for instance in deploy_inst:
        temp = dict()
        temp["Name"] = instance.Inst_Name
        temp["Id"] = instance.Inst_Id
        temp["Ip"] = instance.Inst_Ip
        temp["FQDN"] = instance.Inst_Fqdn
        temp["Command"] = instance.Inst_Cmd
        result["Instances"][instance.Instance] = temp

    deploy_cmds = list(deploy_sheet.deploys_set.all())
    result["DeployCommands"] = []
    for cmd in deploy_cmds:
        temp = dict()
        temp["Instance"] = cmd.Instance.Instance
        temp["Order"] = int(cmd.Order)
        temp["Command"] = cmd.Cmd
        temp["Status"] = int(cmd.Status)
        result["DeployCommands"].append(temp)
    
    json.dump(result, open('test.json', 'w'), indent=2)
    context = {"export_result": json.dumps(result, indent=4)}
    return render(request, 'deploy/export.html', context)

def getAllSheets():
    deploy_sheet = list(models.DeploySheet.objects.all())
    sheet_names = []
    for sheet in deploy_sheet:
        sheet_names.append(sheet.name)
    return sheet_names

def querySheetByName(sheet_name):
    try:
        deploy_sheet = models.DeploySheet.objects.get(name=sheet_name)
    except models.DeploySheet.DoesNotExist:
        return []
    return deploy_sheet


def index(request):
    context = {"sheet_names":getAllSheets()}
    return render(request, 'deploy/index.html', context)


def webhook(request):
    if request.method == 'POST':
        post_table = request.POST
        models.Webhook.objects.create(name=post_table['after'], post_data=str(post_table))
    hook_list = list(models.Webhook.objects.all())
    if not hook_list:
        context = {"content":"this is a test"}
    else:
        context = {"content":hook_list[0].post_data}
    return render(request, 'deploy/webhook.html', context)


def instance(request, sheet_name):
    deploy_sheet = querySheetByName(sheet_name)
    if not deploy_sheet:
        raise Http404("Deploy Sheet does not exist")

    new_item = False
    if request.method == 'POST':
        if request.POST.has_key("counter"):
            selected_instances = list(deploy_sheet.instances_set.all())
            selected_instances[int(request.POST["counter"])-1].delete()
        elif request.POST.has_key('new_item'):
            new_item = request.POST['new_item']
        elif request.POST.has_key("instance"):
            sheet = models.DeploySheet.objects.get(name=sheet_name)
            models.Instances.objects.create(Instance=request.POST["instance"], Inst_Name=request.POST["name"], Inst_Id=request.POST["id"],
                                            Inst_Ip=request.POST["ip"], Inst_Fqdn=request.POST["fqdn"], Inst_Cmd=request.POST["cmd"], sheet=sheet)
    
    selected_instances = list(deploy_sheet.instances_set.all())

    context = {"sheet_names":getAllSheets(),
                "selected_sheet_name":sheet_name,
                "selected_instances":selected_instances,
                "new_item":new_item
               }

    return render(request, 'deploy/index.html', context)

def deploy(request, sheet_name):
    deploy_sheet = querySheetByName(sheet_name)
    if not deploy_sheet:
        raise Http404("Deploy Sheet does not exist")

    new_item = False
    if request.method == 'POST':
        if request.POST.has_key("counter"):
            selected_deploys = list(deploy_sheet.deploys_set.all())
            selected_deploys[int(request.POST["counter"])-1].delete()
        elif request.POST.has_key('new_item'):
            new_item = request.POST['new_item']
        elif request.POST.has_key("instance"):
            sheet = models.DeploySheet.objects.get(name=sheet_name)
            instance = models.Instances.objects.get(Instance=request.POST["instance"])
            models.Deploys.objects.create(Instance=instance, Order=request.POST["order"], Cmd=request.POST["cmd"], Status=request.POST["status"], sheet=sheet)

    selected_deploys = list(deploy_sheet.deploys_set.all())
    
    context = {"sheet_names":getAllSheets(),
               "selected_sheet_name":sheet_name,
               "selected_deploys":selected_deploys,
               "new_item":new_item
              }

    return render(request, 'deploy/deploy.html', context)


def variable(request, sheet_name):
    deploy_sheet = querySheetByName(sheet_name)
    if not deploy_sheet:
        raise Http404("Deploy Sheet does not exist")
    
    new_item = False
    if request.method == 'POST':
        if request.POST.has_key('new_item'):
            new_item = request.POST['new_item']
        elif request.POST.has_key("counter"):
            sel_vars = list(deploy_sheet.variables_set.all())
            sel_vars[int(request.POST["counter"])-1].delete()
        elif request.POST.has_key("attribute") and request.POST["attribute"]:
            try:
                models.Variables.objects.get(Attr_Name=request.POST["attribute"])
            except ObjectDoesNotExist:
                sheet = models.DeploySheet.objects.get(name=sheet_name)
                models.Variables.objects.create(Attr_Name=request.POST["attribute"], Attr_Value=request.POST["value"], sheet=sheet)

    selected_variables = list(deploy_sheet.variables_set.all())

    context = {"sheet_names":getAllSheets(),
               "selected_sheet_name":sheet_name,
               "selected_variables":selected_variables,
               "new_item":new_item
              }

    return render(request, 'deploy/variable.html', context)


def addItem(request):
    if not request.POST.has_key('sheet_name'):
        return render(request, 'deploy/index.html')
    context = {"sheet_name": request.POST['sheet_name']}
    return render(request, 'deploy/addItem.html', context)


def saveItem(request):
    #save the new added item into deploy sheet
    instance = request.POST['instance']
    slave_name = request.POST['slave_name']
    uniq_id = request.POST['uniq_id']
    ip_addr = request.POST['ip_addr']
    fqdn = request.POST['fqdn']
    ecs_command = request.POST['ecs_command']
    if not instance or not slave_name or not uniq_id or not ip_addr:
        context = {"sheet_name": request.POST['sheet_name']}
        return render(request, 'deploy/addItem.html', context)
    if not fqdn:
        fqdn = ip_addr
    sheet = models.DeploySheet.objects.get(name=request.POST['sheet_name'])
    db_ins = models.Instances.objects.create(Instance=instance, Inst_Name=slave_name, Inst_Id=uniq_id, Inst_Ip=ip_addr, Inst_Fqdn=fqdn, Inst_Cmd=ecs_command, sheet=sheet)
    #then, query the whole db to get the deploy sheet and show
    
#    context = {"sheet_name": request.POST['sheet_name']}
#    return render(request, 'deploy/addItem.html', context)

    return render(request, 'deploy/index.html')


def saveVariable(request):
    sheet_name = ""
    if request.POST.has_key('sheet_name'):
        sheet_name = request.POST['sheet_name']
    context = {"sheet_name": sheet_name}
    return render(request, 'deploy/addItem.html', context)

# Create your views here.

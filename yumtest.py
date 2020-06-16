def _list_cves_updateinfo_find(module, pkg):
    cmd = "%s '%s' '%s' '%s' '%s'" % (run_cmd, '-q', 'updateinfo', 'list', 'cves')
    rc, out, err = module.run_command(cmd, encoding=None)
    if rc is 0:
        lines = out.split('\n',1)[-1]
        reach=0
        _pkgs = []
        for line in lines:
            fields = line.strip().split()
            if pkg in line:
                _pkgs.append(fields[2])
            else:
                reach = 1
        if len(_pkgs) > 0:
            msg = ("package %s found" % pkg)
            result = { 'stdout':_pkgs, 'stderr':err, 'rc':0, 'changed':True, 'msg':msg }
            module.exit_json(**result)
        else:
            msg = ("package %s not found" % pkg)
            result = { 'stdout':_pkgs, 'stderr':err, 'rc':0, 'changed':False, 'msg':msg }
            module.exit_json(**result)
    else:
        result = { 'stdout':out, 'stderr':err, 'rc':rc, 'changed':False }
        module.fail_json(**result)

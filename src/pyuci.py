#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Static wrapper for UCI binary:

    batch
    export     [<config>]
    import     [<config>]
    changes    [<config>]
    commit     [<config>]
    add        <config> <section-type>
    add_list   <config>.<section>.<option>=<string>
    del_list   <config>.<section>.<option>=<string>
    show       [<config>[.<section>[.<option>]]]
    get        <config>.<section>[.<option>]
    set        <config>.<section>[.<option>]=<value>
    delete     <config>[.<section>[[.<option>][=<id>]]]
    rename     <config>.<section>[.<option>]=<name>
    revert     <config>[.<section>[.<option>]]
    reorder    <config>.<section>=<position>

    @author: Jiri Slachta
    @version: 0.0.1
"""

import subprocess
import os.path

def uci_call(action, param=None):
    if os.path.exists("/usr/bin/sudo"):
        if param is not None:
            cmd = ["sudo", "uci", action, param]
        else:
            cmd = ["sudo", "uci", action]
    else:
        if param is not None:
            cmd = ["uci", action, param]
        else:
            cmd = ["uci", action]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()

    data = []
    while True:
        line = str(p.stdout.readline()).strip()
        if line != '':
            data.append(line)
        else:
            break

    if len(data) != 0:
        return data[0]
    else:
        return "None"

class uci(object):
        @staticmethod
        def batch():
            """Executes a multi-line UCI script which is typically wrapped into a here document syntax.

            """
            uci_call("batch")

        @staticmethod
        def export_cfg(config=None):
            """Exports the configuration in a machine readable format. It is used internally to
            evaluate configuration files as shell scripts.

            Keyword arguments:
            config -- config file (optional, default None)

            """
            param = config

            return uci_call("export", param)

        @staticmethod
        def import_cfg(config=None):
            """Imports configuration files in UCI syntax.

            Keyword arguments:
            config -- config file (optional, default None)

            """
            param = config
            uci_call("import", param)

        @staticmethod
        def changes(config=None):
            """List staged changes to the given configuration file or if none given, all configuration files.

            Keyword arguments:
            config -- config file (optional, default None)

            """
            param = config
            return uci_call("changes", param)

        @staticmethod
        def commit(config=None):
            """Writes changes of the given configuration file, or if none is given, all configuration files,
            to the filesystem.

            Keyword arguments:
            config -- config file (optional, default None)

            """
            param = config
            uci_call("commit", param)

        @staticmethod
        def add(config, sectionType):
            """Add an anonymous section of type section-type to the given configuration.

            Keyword arguments:
            config      -- config file
            sectionType -- section type

            """

            param = ''.join([config, " ", sectionType])
            uci_call("add", param)

        @staticmethod
        def add_list(config, section, option, string):
            """Add the given string to an existing list option.

            Keyword arguments:
            config  -- config file
            section -- section
            option  -- option
            string  -- string

            uci add_list system.ntp.server='0.de.pool.ntp.org'
            """
            param = ''.join([config, ".", section, ".", option,"=","'"+string+"'"])
            uci_call("add_list", param)

        @staticmethod
        def del_list(config, section, option, string):
            """Deletes the given string from an existing list option.

            Keyword arguments:
            config  -- config file
            section -- section
            option  -- option
            string  -- string

            """
            param = ''.join([config, ".", section, ".", option,"=","'"+string+"'"])
            uci_call("del_list", param)

        @staticmethod
        def show(config=None, section=None, option=None):
            """Show the given option, section or configuration in compressed notation.

            Keyword arguments:
            config  -- config file
            section -- section
            option  -- option

            """

            if (config is not None) and (section is None) and (option is None):
                param = config
            elif (config is not None) and (section is not None) and (option is None):
                param = ''.join([config, ".", section])
            elif (config is not None) and (section is not None) and (option is not None):
                param = ''.join([config, ".", section, ".", option])
            else:
                param = None

            return uci_call("show", param)

        @staticmethod
        def get(config, section, option=None):
            """Get the value of the given option or the type of the given section.

            Keyword arguments:
            config  -- config file
            section -- section
            option  -- option (optional, default None)

            """
            if option is not None:
                param = ''.join([config, ".", section, ".", option])
            else:
                param = ''.join([config, ".", section])

            return uci_call("get", param)

        @staticmethod
        def set(config, section, option=None, value=None):
            """Set the value of the given option, or add a new section with the type set to the given value.

            Keyword arguments:
            config -- config file
            section -- section
            option -- (optional, default None)
            value -- value

            """

            if (option is not None):
                param = ''.join([config, ".", section, ".", option, "=", value])
            else:
                param = ''.join([config, ".", section, "=", value])

            uci_call("set", param)

        @staticmethod
        def delete(config, section=None, option=None, id=None):
            """Delete the given section or option.

            Keyword arguments:
            config -- config file
            section -- section (optional, default None)
            option -- option (optional, default None)
            id -- id (optional, default None)

            """

            if (section is not None) and (option is None) and (id is None):
                param = ''.join([config, ".", section])
            elif (section is not None) and (option is not None) and (id is None):
                param = ''.join([config, ".", section, ".", option])
            else: #all variables are set
                param = ''.join([config, ".", section, ".", option, "=", id])

            uci_call("delete", param)

        @staticmethod
        def rename(config, section, option=None, name=None):
            """Rename the given option or section to the given name.

            Keyword arguments:
            config -- config file
            section -- section
            option -- option (optional)
            name -- name
            <config>.<section>[.<option>]=<name>
            """

            if(option is not None):
                param = ''.join([config, ".", section, ".", option, "=", id])
            else:
                param = ''.join([config, ".", section, "=", id])

            uci_call("rename", param)

        @staticmethod
        def revert(config, section=None, option=None):
            """Revert the given option, section or configuration file.

            Keyword arguments:
            config -- config file
            section -- section (optional)
            option -- option (optional)

            """
            if section is not None and option is None:
                param = ''.join([config, ".", section])
            elif section is not None and option is not None:
                param = ''.join([config, ".", section, ".", option])
            else:
                param=config

            uci_call("revert", param)

        @staticmethod
        def reorder(config, section, position):
            """Reorder the given option, section or configuration file.

            Keyword arguments:
            config -- config file
            section -- section
            position -- position

            """
            param = ''.join([config, ".", section, "=", position])
            uci_call("reorder", param)

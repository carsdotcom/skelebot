[Home](index.md)

---

# HDFS Kerberos

If your project needs to connect to HDFS with Kerberos authentication, Skelebot can handle this very easily.

The scaffolding prompts will request all the needed information for authenticating with kerberos and installing necessary libraries (R and Python). Just make sure you enter (Y/y) when prompted for Kerberos for Hadoop. If you need to add the configuration manually, you can follow this template inside the skelebot.yaml file.

```
...
kerberos:
  hdfsUser: my_hadoop_username
  keytab: path/to/user.keytab
  krbConf: path/to/krb.conf
...
```

The username and keytab fields are fairly straightforward. If you don't know how to generate a keytab, you can follow [this guide](https://www.cloudera.com/documentation/enterprise/5-8-x/topics/cdh_sg_kadmin_kerberos_keytab.html).

The krbConf file is the configuration file for your kerberos setup that must be located in the project directory. More information can be found [here](http://web.mit.edu/kerberos/krb5-1.12/doc/admin/conf_files/krb5_conf.html).

---

<center><< [Artifacts](artifacts.md)  |  [Jupyter](jupyter.md) >></center>

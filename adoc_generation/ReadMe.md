# Swagger2Markup

## Prerequisites

Get the latest Swagger2Markup CLI jar:

* Releases: https://jcenter.bintray.com/io/github/swagger2markup/swagger2markup-cli/

* Snapshots: https://oss.jfrog.org/artifactory/oss-snapshot-local/io/github/swagger2markup/swagger2markup-cli/

## Usage

To create AsciiDoc documentation from a Swagger 2.0 spec:

```shell
$ java -jar ./adoc_generation/swagger2markup-cli-1.3.3.jar convert -f ../docs-server/modules/n1ql/pages/n1ql-rest-api/admin -i admin.yaml -c ./adoc_generation/config.properties
```

Where:

* `-jar` is the location of the Swagger2Markup command line jar.

* `-f` is the location and and name of the AsciiDoc file to output, not including the file extension.

* `-i` is the location and name of the Swagger 2.0 spec.

* `-c` is the location and name of the Swagger2Markup config file.

## Further Information

* [Swagger2Markup Repository](https://github.com/swagger2markup)

* [Swagger2Markup 1.3.3 Documentation](http://swagger2markup.github.io/swagger2markup/1.3.3/)
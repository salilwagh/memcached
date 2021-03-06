import telnetlib
from lib import insert_keys, read_keys, delete_keys


def test_insert_read(node, keyprefix="key", count=50):
    insert_keys(node, keyprefix=keyprefix, count=count)
    read_keys(node, keyprefix=keyprefix, count=count)


def test_insert_read_and_delete(node, keyprefix="key", count=50):
    insert_keys(node, keyprefix=keyprefix, count=count)
    read_keys(node, keyprefix=keyprefix, count=count)
    delete_keys(node, count, keyprefix)


def test_read(node, keyprefix="key", count=50):
    read_keys(node, keyprefix=keyprefix, count=count)


def normal_multinode_operations_scale_up():
    print  "insert and read A series keys via 11211"
    print  "insert, read and delete N series keys via 11211"
    print raw_input("Have you started memcached node(11211)??")
    node11211 = telnetlib.Telnet("localhost", 11211)
    test_insert_read(node11211, keyprefix="A")
    test_insert_read_and_delete(node11211, keyprefix="N")

    print  "read A series keys via 11211 and 11212"
    print  "insert and read B series keys via 11212"
    print  "insert, read and delete N series keys via 11212"
    print raw_input(
        "Have you started added another node(11212)??\nWait for split and migrate to complete")
    node11212 = telnetlib.Telnet("localhost", 11212)
    test_read(node11211, keyprefix="A")
    test_read(node11212, keyprefix="A")

    test_insert_read(node11212, keyprefix="B")

    test_insert_read_and_delete(node11211, keyprefix="N")
    test_insert_read_and_delete(node11212, keyprefix="N")

    print  "read A and B series keys via 11211,11212 and 11213"
    print  "insert and read C series keys via 11213"
    print  "insert, read and delete N series keys via 11213"
    print raw_input(
        "Have you started added another node(11213)??\nWait for split and migrate to complete")
    node11213 = telnetlib.Telnet("localhost", 11213)
    test_read(node11211, keyprefix="A")
    test_read(node11212, keyprefix="A")
    test_read(node11213, keyprefix="A")
    test_read(node11211, keyprefix="B")
    test_read(node11212, keyprefix="B")
    test_read(node11213, keyprefix="B")

    test_insert_read(node11213, keyprefix="C")

    test_insert_read_and_delete(node11211, keyprefix="N")
    test_insert_read_and_delete(node11212, keyprefix="N")
    test_insert_read_and_delete(node11213, keyprefix="N")


def normal_multinode_operations_scale_down():
    node11211 = telnetlib.Telnet("localhost", 11211)
    node11212 = telnetlib.Telnet("localhost", 11212)

    print raw_input(
        "Have you removed 11213 from the cluster??\nWait for merge and migrate to complete")
    test_read(node11211, keyprefix="A")
    test_read(node11212, keyprefix="A")
    test_read(node11211, keyprefix="B")
    test_read(node11212, keyprefix="B")
    test_read(node11211, keyprefix="C")
    test_read(node11212, keyprefix="C")

    test_insert_read_and_delete(node11211, keyprefix="N")
    test_insert_read_and_delete(node11212, keyprefix="N")

    print raw_input(
        "Have you removed 11212 from the cluster??\nWait for merge and migrate to complete")
    test_read(node11211, keyprefix="A")
    test_read(node11211, keyprefix="B")
    test_read(node11211, keyprefix="C")

    test_insert_read_and_delete(node11211, keyprefix="N")


def begin_tests():
    normal_multinode_operations_scale_up()
    normal_multinode_operations_scale_down()

begin_tests()



import iptc

def ban(ip):
    # Create rule with src ip with target of DROP
    rule = iptc.Rule()
    rule.src = ip
    t = rule.create_target("DROP")

    # Inser the ban into the INPUT chain in the FILTER table
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
    chain.insert_rule(rule)


def unban(ip):
    # Disable autocommit on FILTER table to efficiently delete duplicate bans
    table = iptc.Table(iptc.Table.FILTER)
    table.autocommit = False

    # Traverse through INPUT table for rules matching src ip and delete
    chain = iptc.Chain(table, "INPUT")
    for rule in chain.rules:
        if rule.src and ip in rule.src.split('/')[0]:
            chain.delete_rule(rule)
    table.commit()
    table.autocommit = True

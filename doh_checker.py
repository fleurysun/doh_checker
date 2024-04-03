import sys
import asyncio

import httpx
import dns.rcode
import dns.message
import dns.asyncquery
import dns.rdatatype

async def check_wire_format_doh(ip, query_name, post=False, timeout=6):

    query = dns.message.make_query(query_name, dns.rdatatype.A)
    response = None

    async with httpx.AsyncClient(verify=False, http2=True) as client:
        try:
            response = await dns.asyncquery.https(
                query, f"https://{ip}/dns-query", post=post, timeout=timeout, 
                client=client)
        except Exception as e:
            pass

    return True if response is not None else False

async def check_json_doh(ip, query_name, timeout=6):
    response = None

    async with httpx.AsyncClient(verify=False, http2=True) as client:
        try:
            response = await client.get(
                f"https://{ip}/resolve?", timeout=timeout,
                params={"name": query_name, "type": 1})

        except Exception as e:
            pass

    return True if response is not None else False

async def check_doh(ip, query_name, timeout=6):
    results = {}

    results["GETBASE64PARAM"] = await check_wire_format_doh(ip, query_name, timeout)
    
    results["POST"] = await check_wire_format_doh(ip, query_name, True, timeout)

    results["JSON"] = await check_json_doh(ip, query_name, timeout)
    
    return results

if __name__ == "__main__":
    query_name = "google.com"
    timeout = 6

    if len(sys.argv) > 1:
        loop = asyncio.get_event_loop()
        for ip in sys.argv[1:]:
            results = loop.run_until_complete(check_doh(
                ip, query_name, timeout))
            for item in results:
                if results[item]:
                    print(ip, item)
    else:
        print("I need at least a IP")
        print("Usage:", sys.argv[0], "ip_to_be_checked")



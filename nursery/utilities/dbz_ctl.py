import argparse
import json
import sys
import requests

BASE_URL = "http://localhost:8083"

def list_connectors():
    r = requests.get(f"{BASE_URL}/connectors")
    print(json.dumps(r.json(), indent=2))

def get_connector_status(name):
    r = requests.get(f"{BASE_URL}/connectors/{name}/status")
    print(json.dumps(r.json(), indent=2))

def delete_connector(name):
    r = requests.delete(f"{BASE_URL}/connectors/{name}")
    print(f"Deleted connector {name}. Status: {r.status_code}")

def restart_connector(name):
    r = requests.post(f"{BASE_URL}/connectors/{name}/restart")
    print(f"Restarted connector {name}. Status: {r.status_code}")

def create_connector(name, config_file):
    with open(config_file) as f:
        config = json.load(f)
    r = requests.post(f"{BASE_URL}/connectors", json=config)
    if r.status_code in (200, 201):
        print(f"Connector {name} created successfully.")
    else:
        print(f"Error creating connector {name}: {r.status_code}\n{r.text}")
        sys.exit(1)

def sample_config(name):
    print(json.dumps({
        "name": name,
        "config": {
            "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
            "database.hostname": "db",
            "database.port": "5432",
            "database.user": "postgres",
            "database.password": "postgres",
            "database.dbname": "appdb",
            "database.server.name": name,
            "plugin.name": "pgoutput",
            "table.include.list": "public.events",
            "slot.name": f"{name}_slot",
            "publication.name": f"{name}_pub",
            "topic.prefix": f"{name}",
            "key.converter": "org.apache.kafka.connect.json.JsonConverter",
            "value.converter": "org.apache.kafka.connect.json.JsonConverter",
            "key.converter.schemas.enable": "false",
            "value.converter.schemas.enable": "false"
        }
    }, indent=2))

def get_config(name):
    r = requests.get(f"{BASE_URL}/connectors/{name}/config")
    if r.status_code == 200:
        print(json.dumps(r.json(), indent=2))
    else:
        print(f"Failed to get config for {name}: {r.status_code}\n{r.text}")

def main():
    parser = argparse.ArgumentParser(description="Debezium Kafka Connect CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="List connectors")

    status_parser = subparsers.add_parser("status", help="Get connector status")
    status_parser.add_argument("name")

    delete_parser = subparsers.add_parser("delete", help="Delete connector")
    delete_parser.add_argument("name")

    restart_parser = subparsers.add_parser("restart", help="Restart connector")
    restart_parser.add_argument("name")

    create_parser = subparsers.add_parser("create", help="Create connector")
    create_parser.add_argument("name")
    create_parser.add_argument("config_file", help="Path to connector config JSON")

    sample_parser = subparsers.add_parser("sample-config", help="Print a sample Debezium PostgreSQL connector config")
    sample_parser.add_argument("name", help="Connector name")

    get_config_parser = subparsers.add_parser("get-config", help="Get current config of a connector")
    get_config_parser.add_argument("name")

    args = parser.parse_args()

    if args.command == "list":
        list_connectors()
    elif args.command == "status":
        get_connector_status(args.name)
    elif args.command == "delete":
        delete_connector(args.name)
    elif args.command == "restart":
        restart_connector(args.name)
    elif args.command == "create":
        create_connector(args.name, args.config_file)
    elif args.command == "sample-config":
        sample_config(args.name)
    elif args.command == "get-config":
        get_config(args.name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()


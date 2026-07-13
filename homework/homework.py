"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    import glob
    import os
    import zipfile

    import pandas as pd

    input_directory = "files/input/"
    output_directory = "files/output/"

    #
    # Lee y concatena todos los archivos csv.zip presentes en el
    # directorio de entrada, sin necesidad de descomprimirlos primero.
    #
    zip_paths = glob.glob(os.path.join(input_directory, "*.zip"))

    dataframes = []
    for zip_path in zip_paths:
        with zipfile.ZipFile(zip_path) as zip_file:
            for name in zip_file.namelist():
                if name.endswith(".csv"):
                    with zip_file.open(name) as csv_file:
                        dataframes.append(pd.read_csv(csv_file, sep=",", index_col=0))

    df = pd.concat(dataframes, ignore_index=True)
    df = df.drop(columns=["client_id"])
    df = df.reset_index(names="client_id")

    #
    # client.csv
    #
    client = df[
        [
            "client_id",
            "age",
            "job",
            "marital",
            "education",
            "credit_default",
            "mortgage",
        ]
    ].copy()

    client["job"] = client["job"].str.replace(".", "", regex=False)
    client["job"] = client["job"].str.replace("-", "_", regex=False)

    client["education"] = client["education"].str.replace(".", "_", regex=False)
    client["education"] = client["education"].replace("unknown", pd.NA)

    client["credit_default"] = client["credit_default"].apply(
        lambda x: 1 if x == "yes" else 0
    )
    client["mortgage"] = client["mortgage"].apply(lambda x: 1 if x == "yes" else 0)

    #
    # campaign.csv
    #
    campaign = df[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
            "day",
            "month",
        ]
    ].copy()

    campaign["previous_outcome"] = campaign["previous_outcome"].apply(
        lambda x: 1 if x == "success" else 0
    )
    campaign["campaign_outcome"] = campaign["campaign_outcome"].apply(
        lambda x: 1 if x == "yes" else 0
    )

    campaign["month"] = campaign["month"].str.lower()
    month_map = {
        "jan": "01",
        "feb": "02",
        "mar": "03",
        "apr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "aug": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dec": "12",
    }
    campaign["month"] = campaign["month"].map(month_map)
    campaign["day"] = campaign["day"].astype(str).str.zfill(2)

    campaign["last_contact_date"] = (
        "2022" + "-" + campaign["month"] + "-" + campaign["day"]
    )

    campaign = campaign[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
            "last_contact_date",
        ]
    ]

    #
    # economics.csv
    #
    economics = df[
        [
            "client_id",
            "cons_price_idx",
            "euribor_three_months",
        ]
    ].copy()

    #
    # Guarda los archivos generados
    #
    os.makedirs(output_directory, exist_ok=True)

    client.to_csv(os.path.join(output_directory, "client.csv"), index=False)
    campaign.to_csv(os.path.join(output_directory, "campaign.csv"), index=False)
    economics.to_csv(os.path.join(output_directory, "economics.csv"), index=False)


if __name__ == "__main__":
    clean_campaign_data()

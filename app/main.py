from fastapi import FastAPI, Query
from typing import Optional
from dotenv import load_dotenv
import os
import psycopg2


load_dotenv()

app = FastAPI()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

@app.get("/")
def read_root():
    return {"message": "Hello, world"}

@app.get("/db-version")
def db_version():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()[0]
    cur.close()
    conn.close()
    return {"version": version}

@app.get("/pessoa")
def get_pessoas(cpf_cnpj: Optional[str] = Query(None, description="CPF ou CNPJ para filtrar")):
    conn = get_db_connection()
    cur = conn.cursor()

    base_query = """
        SELECT 
            emb.numero_emb,
            emb.cpf_cnpj,
            emb.autuado,
            emb.data_auto
        FROM (
            SELECT
                (embp.numero_ai::text || '-'::text) || embp.serie::text AS numero_emb,
                aip.cpf_cnpj,
                aip.autuado,
                aip.data_auto
            FROM 
                dmif.dmif_areas_embargadas embp
            LEFT JOIN 
                dmif.dmif_autos_infracao aip 
            ON 
                aip.numero_ai::text = embp.numero_ai::text AND aip.serie::text = embp.serie::text
            WHERE 
                embp.st_divulgar IS NOT FALSE
            
            UNION
            
            SELECT      
                embe.num_embargo AS numero_emb,
                embe.cpf_cnpj_autuado AS cpf_cnpj,
                embe.nome_autuado AS autuado,
                to_date(embe.data_lavratura_embargo, 'DD/MM/YYYY'::text) AS data_auto
            FROM 
                dmif.sabia_embargos_eletronicos embe
            WHERE (embe.st_divulga::text <> 'F'::text OR embe.st_divulga IS NULL OR embe.st_divulga::text = ''::text) 
            AND (embe.migracao::text <> 'T'::text OR embe.migracao IS NULL OR embe.migracao::text = ''::text) 
            AND ((embe.status_embargo_aie::text <> ALL (ARRAY['Cancelado'::character varying::text, 'Excluído'::character varying::text])) OR embe.status_embargo_aie IS NULL) 
            AND (embe.sit_desembargo = ''::text OR embe.sit_desembargo IS NULL)
        ) emb
    """

    # Adiciona o filtro, se `cpf_cnpj` foi informado
    if cpf_cnpj:
        base_query += " WHERE emb.cpf_cnpj = %s"
        cur.execute(base_query, (cpf_cnpj,))
    else:
        cur.execute(base_query)

    results = cur.fetchall()
    cur.close()
    conn.close()

    pessoas = [
        {
            "numero_emb": row[0],
            "cpf_cnpj": row[1],
            "autuado": row[2],
            "data_auto": row[3]
        }
        for row in results
    ]
    
    return {"pessoas": pessoas}

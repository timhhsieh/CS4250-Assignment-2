-- Table: public.Documents

-- DROP TABLE IF EXISTS public."Documents";

CREATE TABLE IF NOT EXISTS public."Documents"
(
    doc_id integer NOT NULL,
    category_id integer NOT NULL,
    text text COLLATE pg_catalog."default" NOT NULL,
    title text COLLATE pg_catalog."default" NOT NULL,
    num_chars integer,
    date date NOT NULL,
    CONSTRAINT "Documents_pkey" PRIMARY KEY (doc_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Documents"
    OWNER to postgres;
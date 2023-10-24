-- Table: public.Categories

-- DROP TABLE IF EXISTS public."Categories";

CREATE TABLE IF NOT EXISTS public."Categories"
(
    category_id integer NOT NULL,
    category_name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Categories_pkey" PRIMARY KEY (category_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Categories"
    OWNER to postgres;
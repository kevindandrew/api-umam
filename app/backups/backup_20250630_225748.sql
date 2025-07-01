--
-- PostgreSQL database dump
--

-- Dumped from database version 17.3
-- Dumped by pg_dump version 17.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: aulas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.aulas (
    aula_id integer NOT NULL,
    nombre_aula character varying(50) NOT NULL,
    capacidad integer NOT NULL,
    sucursal_id integer NOT NULL
);


ALTER TABLE public.aulas OWNER TO postgres;

--
-- Name: aulas_aula_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.aulas_aula_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.aulas_aula_id_seq OWNER TO postgres;

--
-- Name: aulas_aula_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.aulas_aula_id_seq OWNED BY public.aulas.aula_id;


--
-- Name: curso_docente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.curso_docente (
    curso_docente_id integer NOT NULL,
    curso_id integer NOT NULL,
    usuario_id integer NOT NULL,
    gestion_id integer NOT NULL
);


ALTER TABLE public.curso_docente OWNER TO postgres;

--
-- Name: curso_docente_curso_docente_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.curso_docente_curso_docente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.curso_docente_curso_docente_id_seq OWNER TO postgres;

--
-- Name: curso_docente_curso_docente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.curso_docente_curso_docente_id_seq OWNED BY public.curso_docente.curso_docente_id;


--
-- Name: curso_sucursal; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.curso_sucursal (
    curso_sucursal_id integer NOT NULL,
    curso_id integer NOT NULL,
    sucursal_id integer NOT NULL,
    gestion_id integer NOT NULL
);


ALTER TABLE public.curso_sucursal OWNER TO postgres;

--
-- Name: curso_sucursal_curso_sucursal_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.curso_sucursal_curso_sucursal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.curso_sucursal_curso_sucursal_id_seq OWNER TO postgres;

--
-- Name: curso_sucursal_curso_sucursal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.curso_sucursal_curso_sucursal_id_seq OWNED BY public.curso_sucursal.curso_sucursal_id;


--
-- Name: cursos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cursos (
    curso_id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    gestoria boolean NOT NULL
);


ALTER TABLE public.cursos OWNER TO postgres;

--
-- Name: cursos_curso_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cursos_curso_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cursos_curso_id_seq OWNER TO postgres;

--
-- Name: cursos_curso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cursos_curso_id_seq OWNED BY public.cursos.curso_id;


--
-- Name: datos_academicos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.datos_academicos (
    academico_id integer NOT NULL,
    estudiante_id integer NOT NULL,
    grado_institucion character varying(100),
    anios_servicio integer,
    ultimo_cargo character varying(100),
    otras_habilidades text
);


ALTER TABLE public.datos_academicos OWNER TO postgres;

--
-- Name: datos_academicos_academico_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.datos_academicos_academico_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.datos_academicos_academico_id_seq OWNER TO postgres;

--
-- Name: datos_academicos_academico_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.datos_academicos_academico_id_seq OWNED BY public.datos_academicos.academico_id;


--
-- Name: datos_familiares; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.datos_familiares (
    familiar_id integer NOT NULL,
    estudiante_id integer NOT NULL,
    tipo character varying(20) NOT NULL,
    ap_paterno character varying(100),
    ap_materno character varying(100),
    nombres character varying(100),
    parentesco character varying(50),
    telefono character varying(20),
    direccion text,
    relacion character varying(50),
    CONSTRAINT datos_familiares_tipo_check CHECK (((tipo)::text = ANY ((ARRAY['referencia'::character varying, 'conviviente'::character varying, 'emergencia'::character varying])::text[])))
);


ALTER TABLE public.datos_familiares OWNER TO postgres;

--
-- Name: datos_familiares_familiar_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.datos_familiares_familiar_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.datos_familiares_familiar_id_seq OWNER TO postgres;

--
-- Name: datos_familiares_familiar_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.datos_familiares_familiar_id_seq OWNED BY public.datos_familiares.familiar_id;


--
-- Name: datos_medicos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.datos_medicos (
    medico_id integer NOT NULL,
    estudiante_id integer NOT NULL,
    sistema_salud character varying(100),
    frecuencia_medico character varying(100),
    enfermedad_base text,
    alergias text,
    tratamiento_especifico text,
    tuvo_covid boolean
);


ALTER TABLE public.datos_medicos OWNER TO postgres;

--
-- Name: datos_medicos_medico_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.datos_medicos_medico_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.datos_medicos_medico_id_seq OWNER TO postgres;

--
-- Name: datos_medicos_medico_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.datos_medicos_medico_id_seq OWNED BY public.datos_medicos.medico_id;


--
-- Name: dias_clase; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dias_clase (
    dia_clase_id integer NOT NULL,
    horario_id integer NOT NULL,
    dia_semana_id integer NOT NULL,
    hora_id integer NOT NULL
);


ALTER TABLE public.dias_clase OWNER TO postgres;

--
-- Name: dias_clase_dia_clase_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dias_clase_dia_clase_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dias_clase_dia_clase_id_seq OWNER TO postgres;

--
-- Name: dias_clase_dia_clase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dias_clase_dia_clase_id_seq OWNED BY public.dias_clase.dia_clase_id;


--
-- Name: dias_semana; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dias_semana (
    dias_semana_id integer NOT NULL,
    dia_semana character varying(10) NOT NULL
);


ALTER TABLE public.dias_semana OWNER TO postgres;

--
-- Name: dias_semana_dias_semana_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dias_semana_dias_semana_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dias_semana_dias_semana_id_seq OWNER TO postgres;

--
-- Name: dias_semana_dias_semana_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dias_semana_dias_semana_id_seq OWNED BY public.dias_semana.dias_semana_id;


--
-- Name: estudiantes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.estudiantes (
    estudiante_id integer NOT NULL,
    nombres character varying(100) NOT NULL,
    ap_paterno character varying(100) NOT NULL,
    ap_materno character varying(100) NOT NULL,
    ci character varying(20) NOT NULL,
    telefono character varying(20),
    fecha_nacimiento date,
    genero character varying(20),
    lugar_nacimiento character varying(100),
    estado_civil character varying(50),
    direccion text,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    como_se_entero character varying(100)
);


ALTER TABLE public.estudiantes OWNER TO postgres;

--
-- Name: estudiantes_estudiante_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.estudiantes_estudiante_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.estudiantes_estudiante_id_seq OWNER TO postgres;

--
-- Name: estudiantes_estudiante_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.estudiantes_estudiante_id_seq OWNED BY public.estudiantes.estudiante_id;


--
-- Name: gestion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gestion (
    gestion_id integer NOT NULL,
    gestion character varying(50) NOT NULL,
    year_id integer NOT NULL
);


ALTER TABLE public.gestion OWNER TO postgres;

--
-- Name: gestion_gestion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.gestion_gestion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gestion_gestion_id_seq OWNER TO postgres;

--
-- Name: gestion_gestion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.gestion_gestion_id_seq OWNED BY public.gestion.gestion_id;


--
-- Name: hora; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hora (
    hora_id integer NOT NULL,
    hora_inicio time without time zone NOT NULL,
    hora_fin time without time zone NOT NULL,
    CONSTRAINT check_hora_valida CHECK ((hora_fin > hora_inicio))
);


ALTER TABLE public.hora OWNER TO postgres;

--
-- Name: hora_hora_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.hora_hora_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.hora_hora_id_seq OWNER TO postgres;

--
-- Name: hora_hora_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.hora_hora_id_seq OWNED BY public.hora.hora_id;


--
-- Name: horarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.horarios (
    horario_id integer NOT NULL,
    curso_id integer NOT NULL,
    aula_id integer NOT NULL,
    profesor_id integer NOT NULL,
    gestion_id integer NOT NULL,
    activo boolean DEFAULT true
);


ALTER TABLE public.horarios OWNER TO postgres;

--
-- Name: horarios_horario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.horarios_horario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.horarios_horario_id_seq OWNER TO postgres;

--
-- Name: horarios_horario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.horarios_horario_id_seq OWNED BY public.horarios.horario_id;


--
-- Name: matriculas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.matriculas (
    matricula_id integer NOT NULL,
    estudiante_id integer NOT NULL,
    horario_id integer NOT NULL,
    gestion_id integer NOT NULL,
    fecha_matricula timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    nota_final numeric(5,2),
    estado character varying(20) DEFAULT 'activo'::character varying
);


ALTER TABLE public.matriculas OWNER TO postgres;

--
-- Name: matriculas_matricula_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.matriculas_matricula_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.matriculas_matricula_id_seq OWNER TO postgres;

--
-- Name: matriculas_matricula_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.matriculas_matricula_id_seq OWNED BY public.matriculas.matricula_id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    rol_id integer NOT NULL,
    nombre character varying(20) NOT NULL
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: roles_rol_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_rol_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_rol_id_seq OWNER TO postgres;

--
-- Name: roles_rol_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_rol_id_seq OWNED BY public.roles.rol_id;


--
-- Name: sucursales; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sucursales (
    sucursal_id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    direccion text NOT NULL
);


ALTER TABLE public.sucursales OWNER TO postgres;

--
-- Name: sucursales_sucursal_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sucursales_sucursal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sucursales_sucursal_id_seq OWNER TO postgres;

--
-- Name: sucursales_sucursal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sucursales_sucursal_id_seq OWNED BY public.sucursales.sucursal_id;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    usuario_id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(255) NOT NULL,
    nombres character varying(100) NOT NULL,
    ap_paterno character varying(100) NOT NULL,
    ap_materno character varying(100) NOT NULL,
    ci character varying(20) NOT NULL,
    telefono character varying(20),
    rol_id integer NOT NULL,
    sucursal_id integer
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: usuarios_usuario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_usuario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_usuario_id_seq OWNER TO postgres;

--
-- Name: usuarios_usuario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_usuario_id_seq OWNED BY public.usuarios.usuario_id;


--
-- Name: year; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.year (
    year_id integer NOT NULL,
    year character varying(50) NOT NULL
);


ALTER TABLE public.year OWNER TO postgres;

--
-- Name: year_year_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.year_year_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.year_year_id_seq OWNER TO postgres;

--
-- Name: year_year_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.year_year_id_seq OWNED BY public.year.year_id;


--
-- Name: aulas aula_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aulas ALTER COLUMN aula_id SET DEFAULT nextval('public.aulas_aula_id_seq'::regclass);


--
-- Name: curso_docente curso_docente_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curso_docente ALTER COLUMN curso_docente_id SET DEFAULT nextval('public.curso_docente_curso_docente_id_seq'::regclass);


--
-- Name: curso_sucursal curso_sucursal_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curso_sucursal ALTER COLUMN curso_sucursal_id SET DEFAULT nextval('public.curso_sucursal_curso_sucursal_id_seq'::regclass);


--
-- Name: cursos curso_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cursos ALTER COLUMN curso_id SET DEFAULT nextval('public.cursos_curso_id_seq'::regclass);


--
-- Name: datos_academicos academico_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datos_academicos ALTER COLUMN academico_id SET DEFAULT nextval('public.datos_academicos_academico_id_seq'::regclass);


--
-- Name: datos_familiares familiar_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datos_familiares ALTER COLUMN familiar_id SET DEFAULT nextval('public.datos_familiares_familiar_id_seq'::regclass);


--
-- Name: datos_medicos medico_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datos_medicos ALTER COLUMN medico_id SET DEFAULT nextval('public.datos_medicos_medico_id_seq'::regclass);


--
-- Name: dias_clase dia_clase_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dias_clase ALTER COLUMN dia_clase_id SET DEFAULT nextval('public.dias_clase_dia_clase_id_seq'::regclass);


--
-- Name: dias_semana dias_semana_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dias_semana ALTER COLUMN dias_semana_id SET DEFAULT nextval('public.dias_semana_dias_semana_id_seq'::regclass);


--
-- Name: estudiantes estudiante_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estudiantes ALTER COLUMN estudiante_id SET DEFAULT nextval('public.estudiantes_estudiante_id_seq'::regclass);


--
-- Name: gestion gestion_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gestion ALTER COLUMN gestion_id SET DEFAULT nextval('public.gestion_gestion_id_seq'::regclass);


--
-- Name: hora hora_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hora ALTER COLUMN hora_id SET DEFAULT nextval('public.hora_hora_id_seq'::regclass);


--
-- Name: horarios horario_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horarios ALTER COLUMN horario_id SET DEFAULT nextval('public.horarios_horario_id_seq'::regclass);


--
-- Name: matriculas matricula_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.matriculas ALTER COLUMN matricula_id SET DEFAULT nextval('public.matriculas_matricula_id_seq'::regclass);


--
-- Name: roles rol_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN rol_id SET DEFAULT nextval('public.roles_rol_id_seq'::regclass);


--
-- Name: sucursales sucursal_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sucursales ALTER COLUMN sucursal_id SET DEFAULT nextval('public.sucursales_sucursal_id_seq'::regclass);


--
-- Name: usuarios usuario_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN usuario_id SET DEFAULT nextval('public.usuarios_usuario_id_seq'::regclass);


--
-- Name: year year_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.year ALTER COLUMN year_id SET DEFAULT nextval('public.year_year_id_seq'::regclass);


--
-- Data for Name: aulas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.aulas (aula_id, nombre_aula, capacidad, sucursal_id) FROM stdin;
1	Aula 101	30	1
2	Aula 201	25	1
3	Aula 102	20	2
4	Laboratorio	15	3
\.


--
-- Data for Name: curso_docente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.curso_docente (curso_docente_id, curso_id, usuario_id, gestion_id) FROM stdin;
1	1	3	1
2	2	4	1
3	3	3	2
4	1	3	3
\.


--
-- Data for Name: curso_sucursal; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.curso_sucursal (curso_sucursal_id, curso_id, sucursal_id, gestion_id) FROM stdin;
1	1	1	1
2	2	3	1
3	3	1	2
4	4	2	3
\.


--
-- Data for Name: cursos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cursos (curso_id, nombre, gestoria) FROM stdin;
1	Matemáticas Básicas	f
2	Lenguaje y Comunicación	f
3	Gestión Empresarial	t
4	Ciencias Naturales	f
\.


--
-- Data for Name: datos_academicos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.datos_academicos (academico_id, estudiante_id, grado_institucion, anios_servicio, ultimo_cargo, otras_habilidades) FROM stdin;
1	1	Bachiller	0	\N	Inglés intermedio
2	2	Técnico Medio	2	Asistente administrativo	Excel avanzado
3	3	Bachiller	1	Vendedor	\N
6	7	Colegio Nacional	4	Delegado	Inglés, informática
9	8	Universidad Privada	2	Asistente Contable	Photoshop, Excel Avanzado
10	8	Instituto Técnico	1	Practicante	Mecánica básica
11	9	Colegio Nacional	4	Delegado	Inglés, informática
\.


--
-- Data for Name: datos_familiares; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.datos_familiares (familiar_id, estudiante_id, tipo, ap_paterno, ap_materno, nombres, parentesco, telefono, direccion, relacion) FROM stdin;
2	2	referencia	Gutiérrez	López	Juan	Tío	77733445	Calle Jordán #789	Contacto emergencia
6	7	referencia	Rojas	Lopez	Juan	Padre	78965412	Zona Norte	Buena
1	1	conviviente	Fernández	Pérez	María	Madre	77711223	Av. Arce #456	Responsable
3	3	conviviente	Vargas	Gómez	Carlos	Padre	77755667	Av. San Martín #101	Responsable
9	8	referencia	Gómez	López	Carlos Alberto	Padre	70012345	Av. Circunvalación #123	Buena
10	8	emergencia	Gómez	Fernández	Ana María	Hermana	71234567	Calle Junín #456	Excelente
11	9	referencia	Rojas	Lopez	Juan	Padre	78965412	Zona Norte	Buena
\.


--
-- Data for Name: datos_medicos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.datos_medicos (medico_id, estudiante_id, sistema_salud, frecuencia_medico, enfermedad_base, alergias, tratamiento_especifico, tuvo_covid) FROM stdin;
1	1	Seguro privado	Anual	\N	Penicilina	\N	t
2	2	Caja de salud	Solo emergencias	Asma	Polvo	Inhalador	f
3	3	Ninguno	Nunca	\N	\N	\N	t
4	7	Caja Nacional	Mensual	Ninguna	Polvo	Antialérgicos	f
6	8	Seguro Privado	Trimestral	Asma leve	Ninguna	Inhalador ocasional	t
7	9	Caja Nacional	Mensual	Ninguna	Polvo	Antialérgicos	f
\.


--
-- Data for Name: dias_clase; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dias_clase (dia_clase_id, horario_id, dia_semana_id, hora_id) FROM stdin;
5	4	5	3
\.


--
-- Data for Name: dias_semana; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dias_semana (dias_semana_id, dia_semana) FROM stdin;
1	Lunes
2	Martes
3	Miércoles
4	Jueves
5	Viernes
6	Sábado
\.


--
-- Data for Name: estudiantes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.estudiantes (estudiante_id, nombres, ap_paterno, ap_materno, ci, telefono, fecha_nacimiento, genero, lugar_nacimiento, estado_civil, direccion, fecha_registro, como_se_entero) FROM stdin;
1	Luis	Fernández	Rojas	8899001	77788990	2000-05-15	Masculino	La Paz	Soltero	Av. Arce #456	2025-05-22 19:43:41.4142	Redes Sociales
2	Sofía	Gutiérrez	Mendoza	9988112	77799881	1999-08-22	Femenino	Cochabamba	Soltero	Calle Jordán #789	2025-05-22 19:43:41.4142	Recomendación
3	Pedro	Vargas	Salinas	7788993	77777889	2001-03-10	Masculino	Santa Cruz	Soltero	Av. San Martín #101	2025-05-22 19:43:41.4142	Publicidad
6	Ana María	Perez	Gonzales	87654321	67891234	1995-05-15	Femenino	Santa Cruz	Casado	Calle Jordán #123	2025-06-16 03:20:24.62889	Recomendación de un amigo
7	Kevin	Rojas	Flores	12345678	71234567	2003-09-20	Masculino	Cochabamba	Soltero	Av. Blanco Galindo	2025-06-16 03:42:37.122904	Facebook
8	María Luisilla	Gómez	Martínez	9876543	67891234	1998-11-15	Femenino	Santa Cruz	Casado	Zona Sur, Calle 5 #789	2025-06-16 04:05:40.138523	Instagram
9	CHente	Rojas	Flores	12345678543543	71234567	2003-09-20	Masculino	Cochabamba	Soltero	Av. Blanco Galindo	2025-06-16 05:01:43.390952	Facebook
\.


--
-- Data for Name: gestion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gestion (gestion_id, gestion, year_id) FROM stdin;
1	Gestión I-2023	1
2	Gestión II-2023	1
3	Gestión I-2024	2
4	Gestión II-2024	2
5	Gestión I-2025	3
\.


--
-- Data for Name: hora; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.hora (hora_id, hora_inicio, hora_fin) FROM stdin;
1	08:00:00	10:00:00
2	10:30:00	12:30:00
3	14:00:00	16:00:00
4	16:30:00	18:30:00
\.


--
-- Data for Name: horarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.horarios (horario_id, curso_id, aula_id, profesor_id, gestion_id, activo) FROM stdin;
4	4	3	4	3	t
\.


--
-- Data for Name: matriculas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.matriculas (matricula_id, estudiante_id, horario_id, gestion_id, fecha_matricula, nota_final, estado) FROM stdin;
3	3	4	3	2025-05-22 19:44:03.83228	\N	activo
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (rol_id, nombre) FROM stdin;
1	administrador
2	encargado_sucursal
3	facilitador
\.


--
-- Data for Name: sucursales; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sucursales (sucursal_id, nombre, direccion) FROM stdin;
1	Sucursal Central	Av. Principal #123, Zona Centro
2	Sucursal Norte	Av. Circunvalación #456, Zona Norte
3	Sucursal Sur	Calle Junín #789, Zona Sur
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (usuario_id, username, password, nombres, ap_paterno, ap_materno, ci, telefono, rol_id, sucursal_id) FROM stdin;
1	admin	hashed_password_123	Juan	Pérez	Gómez	1234567	77712345	1	1
2	encargado_norte	hashed_password_456	María	López	Fernández	7654321	77754321	2	2
3	prof_math	hashed_password_789	Carlos	García	Vargas	1122334	77711223	3	1
4	prof_lenguaje	hashed_password_101	Ana	Martínez	Díaz	4433221	77744332	3	3
6	belucita	$2b$12$cYb83VpDWtrl7QwHisNRjuSPhkii0dZxjKxfxN0oWs667mnz.eE9O	belen	segales	ramos	123456123	1234567	1	\N
7	kevindandrew	123789345	juanito	perez	mamani	12345678922	12388844	3	\N
8	pedrito	$2b$12$lnZ028aBY9Sf8.aCAAqxEO48dcqq94mizdHZoVdSmWT8ZYsCEUsBq	pepillo	asdasdasd	asdasdsa	9238479823	81276378312	1	\N
\.


--
-- Data for Name: year; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.year (year_id, year) FROM stdin;
1	2023
2	2024
3	2025
\.


--
-- Name: aulas_aula_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.aulas_aula_id_seq', 4, true);


--
-- Name: curso_docente_curso_docente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.curso_docente_curso_docente_id_seq', 4, true);


--
-- Name: curso_sucursal_curso_sucursal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.curso_sucursal_curso_sucursal_id_seq', 4, true);


--
-- Name: cursos_curso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cursos_curso_id_seq', 4, true);


--
-- Name: datos_academicos_academico_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.datos_academicos_academico_id_seq', 11, true);


--
-- Name: datos_familiares_familiar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.datos_familiares_familiar_id_seq', 11, true);


--
-- Name: datos_medicos_medico_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.datos_medicos_medico_id_seq', 7, true);


--
-- Name: dias_clase_dia_clase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dias_clase_dia_clase_id_seq', 5, true);


--
-- Name: dias_semana_dias_semana_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dias_semana_dias_semana_id_seq', 6, true);


--
-- Name: estudiantes_estudiante_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.estudiantes_estudiante_id_seq', 9, true);


--
-- Name: gestion_gestion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.gestion_gestion_id_seq', 5, true);


--
-- Name: hora_hora_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.hora_hora_id_seq', 4, true);


--
-- Name: horarios_horario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.horarios_horario_id_seq', 4, true);


--
-- Name: matriculas_matricula_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.matriculas_matricula_id_seq', 3, true);


--
-- Name: roles_rol_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_rol_id_seq', 3, true);


--
-- Name: sucursales_sucursal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sucursales_sucursal_id_seq', 3, true);


--
-- Name: usuarios_usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_usuario_id_seq', 8, true);


--
-- Name: year_year_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.year_year_id_seq', 3, true);


--
-- Name: aulas aulas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aulas
    ADD CONSTRAINT aulas_pkey PRIMARY KEY (aula_id);


--
-- Name: curso_docente curso_docente_curso_id_usuario_id_gestion_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curso_docente
    ADD CONSTRAINT curso_docente_curso_id_usuario_id_gestion_id_key UNIQUE (curso_id, usuario_id, gestion_id);


--
-- Name: curso_docente curso_docente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curso_docente
    ADD CONSTRAINT curso_docente_pkey PRIMARY KEY (curso_docente_id);


--
-- Name: curso_sucursal curso_sucursal_curso_id_sucursal_id_gestion_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curso_sucursal
    ADD CONSTRAINT curso_sucursal_curso_id_sucursal_id_gestion_id_key UNIQUE (curso_id, sucursal_id, gestion_id);


--
-- Name: curso_sucursal curso_sucursal_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curso_sucursal
    ADD CONSTRAINT curso_sucursal_pkey PRIMARY KEY (curso_sucursal_id);


--
-- Name: cursos cursos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cursos
    ADD CONSTRAINT cursos_pkey PRIMARY KEY (curso_id);


--
-- Name: datos_academicos datos_academicos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datos_academicos
    ADD CONSTRAINT datos_academicos_pkey PRIMARY KEY (academico_id);


--
-- Name: datos_familiares datos_familiares_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datos_familiares
    ADD CONSTRAINT datos_familiares_pkey PRIMARY KEY (familiar_id);


--
-- Name: datos_medicos datos_medicos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datos_medicos
    ADD CONSTRAINT datos_medicos_pkey PRIMARY KEY (medico_id);


--
-- Name: dias_clase dias_clase_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dias_clase
    ADD CONSTRAINT dias_clase_pkey PRIMARY KEY (dia_clase_id);


--
-- Name: dias_semana dias_semana_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dias_semana
    ADD CONSTRAINT dias_semana_pkey PRIMARY KEY (dias_semana_id);


--
-- Name: estudiantes estudiantes_ci_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estudiantes
    ADD CONSTRAINT estudiantes_ci_key UNIQUE (ci);


--
-- Name: estudiantes estudiantes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estudiantes
    ADD CONSTRAINT estudiantes_pkey PRIMARY KEY (estudiante_id);


--
-- Name: gestion gestion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gestion
    ADD CONSTRAINT gestion_pkey PRIMARY KEY (gestion_id);


--
-- Name: hora hora_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hora
    ADD CONSTRAINT hora_pkey PRIMARY KEY (hora_id);


--
-- Name: horarios horarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horarios
    ADD CONSTRAINT horarios_pkey PRIMARY KEY (horario_id);


--
-- Name: matriculas matriculas_estudiante_id_horario_id_gestion_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.matriculas
    ADD CONSTRAINT matriculas_estudiante_id_horario_id_gestion_id_key UNIQUE (estudiante_id, horario_id, gestion_id);


--
-- Name: matriculas matriculas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.matriculas
    ADD CONSTRAINT matriculas_pkey PRIMARY KEY (matricula_id);


--
-- Name: roles roles_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_nombre_key UNIQUE (nombre);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (rol_id);


--
-- Name: sucursales sucursales_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sucursales
    ADD CONSTRAINT sucursales_pkey PRIMARY KEY (sucursal_id);


--
-- Name: usuarios usuarios_ci_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_ci_key UNIQUE (ci);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (usuario_id);


--
-- Name: usuarios usuarios_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_username_key UNIQUE (username);


--
-- Name: year year_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.year
    ADD CONSTRAINT year_pkey PRIMARY KEY (year_id);


--
-- Name: aulas aulas_sucursal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aulas
    ADD CONSTRAINT aulas_sucursal_id_fkey FOREIGN KEY (sucursal_id) REFERENCES public.sucursales(sucursal_id);


--
-- Name: curso_docente curso_docente_curso_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curso_docente
    ADD CONSTRAINT curso_docente_curso_id_fkey FOREIGN KEY (curso_id) REFERENCES public.cursos(curso_id);


--
-- Name: curso_docente curso_docente_gestion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curso_docente
    ADD CONSTRAINT curso_docente_gestion_id_fkey FOREIGN KEY (gestion_id) REFERENCES public.gestion(gestion_id);


--
-- Name: curso_docente curso_docente_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curso_docente
    ADD CONSTRAINT curso_docente_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(usuario_id);


--
-- Name: curso_sucursal curso_sucursal_curso_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curso_sucursal
    ADD CONSTRAINT curso_sucursal_curso_id_fkey FOREIGN KEY (curso_id) REFERENCES public.cursos(curso_id);


--
-- Name: curso_sucursal curso_sucursal_gestion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curso_sucursal
    ADD CONSTRAINT curso_sucursal_gestion_id_fkey FOREIGN KEY (gestion_id) REFERENCES public.gestion(gestion_id);


--
-- Name: curso_sucursal curso_sucursal_sucursal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curso_sucursal
    ADD CONSTRAINT curso_sucursal_sucursal_id_fkey FOREIGN KEY (sucursal_id) REFERENCES public.sucursales(sucursal_id);


--
-- Name: datos_academicos datos_academicos_estudiante_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datos_academicos
    ADD CONSTRAINT datos_academicos_estudiante_id_fkey FOREIGN KEY (estudiante_id) REFERENCES public.estudiantes(estudiante_id);


--
-- Name: datos_familiares datos_familiares_estudiante_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datos_familiares
    ADD CONSTRAINT datos_familiares_estudiante_id_fkey FOREIGN KEY (estudiante_id) REFERENCES public.estudiantes(estudiante_id);


--
-- Name: datos_medicos datos_medicos_estudiante_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datos_medicos
    ADD CONSTRAINT datos_medicos_estudiante_id_fkey FOREIGN KEY (estudiante_id) REFERENCES public.estudiantes(estudiante_id);


--
-- Name: dias_clase dias_clase_dia_semana_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dias_clase
    ADD CONSTRAINT dias_clase_dia_semana_id_fkey FOREIGN KEY (dia_semana_id) REFERENCES public.dias_semana(dias_semana_id);


--
-- Name: dias_clase dias_clase_hora_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dias_clase
    ADD CONSTRAINT dias_clase_hora_id_fkey FOREIGN KEY (hora_id) REFERENCES public.hora(hora_id);


--
-- Name: dias_clase dias_clase_horario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dias_clase
    ADD CONSTRAINT dias_clase_horario_id_fkey FOREIGN KEY (horario_id) REFERENCES public.horarios(horario_id);


--
-- Name: gestion gestion_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gestion
    ADD CONSTRAINT gestion_year_id_fkey FOREIGN KEY (year_id) REFERENCES public.year(year_id);


--
-- Name: horarios horarios_aula_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horarios
    ADD CONSTRAINT horarios_aula_id_fkey FOREIGN KEY (aula_id) REFERENCES public.aulas(aula_id);


--
-- Name: horarios horarios_curso_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horarios
    ADD CONSTRAINT horarios_curso_id_fkey FOREIGN KEY (curso_id) REFERENCES public.cursos(curso_id);


--
-- Name: horarios horarios_gestion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horarios
    ADD CONSTRAINT horarios_gestion_id_fkey FOREIGN KEY (gestion_id) REFERENCES public.gestion(gestion_id);


--
-- Name: horarios horarios_profesor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horarios
    ADD CONSTRAINT horarios_profesor_id_fkey FOREIGN KEY (profesor_id) REFERENCES public.usuarios(usuario_id);


--
-- Name: matriculas matriculas_estudiante_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.matriculas
    ADD CONSTRAINT matriculas_estudiante_id_fkey FOREIGN KEY (estudiante_id) REFERENCES public.estudiantes(estudiante_id);


--
-- Name: matriculas matriculas_gestion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.matriculas
    ADD CONSTRAINT matriculas_gestion_id_fkey FOREIGN KEY (gestion_id) REFERENCES public.gestion(gestion_id);


--
-- Name: matriculas matriculas_horario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.matriculas
    ADD CONSTRAINT matriculas_horario_id_fkey FOREIGN KEY (horario_id) REFERENCES public.horarios(horario_id);


--
-- Name: usuarios usuarios_rol_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_rol_id_fkey FOREIGN KEY (rol_id) REFERENCES public.roles(rol_id);


--
-- Name: usuarios usuarios_sucursal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_sucursal_id_fkey FOREIGN KEY (sucursal_id) REFERENCES public.sucursales(sucursal_id);


--
-- PostgreSQL database dump complete
--


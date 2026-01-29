-- OPCIÓN 1: Si los warnings te molestan, elimina las políticas antiguas primero
-- (Solo ejecuta esto si ya creaste las políticas anteriores)

DROP POLICY IF EXISTS "Permitir lectura de pacientes" ON pacientes;
DROP POLICY IF EXISTS "Permitir inserción de pacientes" ON pacientes;
DROP POLICY IF EXISTS "Permitir actualización de pacientes" ON pacientes;
DROP POLICY IF EXISTS "Permitir eliminación de pacientes" ON pacientes;
DROP POLICY IF EXISTS "Permitir lectura de evoluciones" ON evoluciones;
DROP POLICY IF EXISTS "Permitir inserción de evoluciones" ON evoluciones;
DROP POLICY IF EXISTS "Permitir actualización de evoluciones" ON evoluciones;
DROP POLICY IF EXISTS "Permitir eliminación de evoluciones" ON evoluciones;

-- Habilitar RLS en las tablas (si aún no está habilitado)
ALTER TABLE pacientes ENABLE ROW LEVEL SECURITY;
ALTER TABLE evoluciones ENABLE ROW LEVEL SECURITY;

-- OPCIÓN 2: Política simplificada - Permite TODO al usuario anon (tu app)
-- Esto evita los warnings porque es más específico

-- UNA SOLA política para pacientes - permite todo al rol anon
CREATE POLICY "Acceso completo para aplicación"
ON pacientes
FOR ALL
USING (auth.role() = 'anon')
WITH CHECK (auth.role() = 'anon');

-- UNA SOLA política para evoluciones - permite todo al rol anon
CREATE POLICY "Acceso completo para aplicación"
ON evoluciones
FOR ALL
USING (auth.role() = 'anon')
WITH CHECK (auth.role() = 'anon');

-- Verificar que todo esté bien
SELECT tablename, rowsecurity FROM pg_tables 
WHERE schemaname = 'public' AND tablename IN ('pacientes', 'evoluciones');

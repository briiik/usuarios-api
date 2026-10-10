# Pruebas locales completas para usuarios-api (Node.js / Express)
$BaseUrl = "http://localhost:3000"
$ErrorActionPreference = "Stop"

function Invoke-ApiTest {
    param(
        [string]$Method,
        [string]$Path,
        [string]$Body = "",
        [int[]]$ExpectedStatus = @(200),
        [string]$Description = ""
    )

    Write-Host "`n>>> [$Method] $Path" -ForegroundColor White
    Write-Host "    $Description" -ForegroundColor Gray

    $params = @{
        Uri             = "$BaseUrl$Path"
        Method          = $Method
        UseBasicParsing = $true
    }

    if (-not [string]::IsNullOrEmpty($Body)) {
        $params.Body = $Body
        $params.ContentType = "application/json; charset=utf-8"
    }

    try {
        $response = Invoke-WebRequest @params
        $status = [int]$response.StatusCode

        Write-Host "HTTP $status" -ForegroundColor Green

        $data = $null
        if ($response.Content) {
            try {
                $data = $response.Content | ConvertFrom-Json
                Write-Host ($data | ConvertTo-Json -Depth 10)
            } catch {
                Write-Host "Respuesta binaria o archivo descargado (Tamaño: $($response.RawContentLength) bytes)" -ForegroundColor Cyan
            }
        }

        if ($status -notin $ExpectedStatus) {
            throw "Estado inesperado: $status. Se esperaba: $($ExpectedStatus -join ', ')"
        }

        return $data
    }
    catch {
        Write-Host "PRUEBA FALLIDA: $($_.Exception.Message)" -ForegroundColor Red
        throw
    }
}

try {
    Write-Host "`n==================================================" -ForegroundColor Cyan
    Write-Host " INICIANDO PRUEBAS COMPLETAS DE USUARIOS-API" -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Cyan

    $timestamp = [guid]::NewGuid().ToString('N').Substring(0,8)

    # 1. Comprobar salud del servidor
    Invoke-ApiTest -Method "GET" -Path "/" -ExpectedStatus @(200) -Description "Verificar estado del servidor" | Out-Null

    # 2. Crear rol
    $rolBody = @{ nombre = "Administrador-$timestamp" } | ConvertTo-Json
    $rolRes = Invoke-ApiTest -Method "POST" -Path "/api/roles" -Body $rolBody -ExpectedStatus @(201) -Description "Crear nuevo rol"
    $rolId = [int]$rolRes.data[0].id
    Write-Host "ID del rol creado: $rolId" -ForegroundColor Cyan

    # 3. Listar roles
    Invoke-ApiTest -Method "GET" -Path "/api/roles" -ExpectedStatus @(200) -Description "Listar todos los roles" | Out-Null

    # 4. Consultar rol por ID
    Invoke-ApiTest -Method "GET" -Path "/api/roles/$rolId" -ExpectedStatus @(200) -Description "Consultar rol por identificador" | Out-Null

    # 5. Actualizar rol
    $rolUpdateBody = @{ nombre = "Administrador Global-$timestamp" } | ConvertTo-Json
    Invoke-ApiTest -Method "PUT" -Path "/api/roles/$rolId" -Body $rolUpdateBody -ExpectedStatus @(200) -Description "Actualizar rol existente" | Out-Null

    # 6. Crear usuario asociado al rol
    $userBody = @{
        nombre   = "Maria Lopez"
        correo   = "maria-$timestamp@empresa.com"
        password = "PasswordSeguro123"
        rolId    = $rolId
    } | ConvertTo-Json
    $userRes = Invoke-ApiTest -Method "POST" -Path "/api/usuarios" -Body $userBody -ExpectedStatus @(201) -Description "Registrar usuario asociado al rol"
    $usuarioId = [int]$userRes.data[0].id
    Write-Host "ID del usuario creado: $usuarioId" -ForegroundColor Cyan

    # 7. Listar usuarios
    Invoke-ApiTest -Method "GET" -Path "/api/usuarios" -ExpectedStatus @(200) -Description "Listar todos los usuarios" | Out-Null

    # 8. Consultar usuario por ID
    Invoke-ApiTest -Method "GET" -Path "/api/usuarios/$usuarioId" -ExpectedStatus @(200) -Description "Consultar usuario existente" | Out-Null

    # 9. Actualizar usuario
    $userUpdateBody = @{
        nombre = "Maria Lopez Actualizada"
        correo = "maria-actualizada-$timestamp@empresa.com"
    } | ConvertTo-Json
    Invoke-ApiTest -Method "PUT" -Path "/api/usuarios/$usuarioId" -Body $userUpdateBody -ExpectedStatus @(200) -Description "Actualizar datos del usuario" | Out-Null

    # 10. Eliminar usuario (antes del rol)
    Invoke-ApiTest -Method "DELETE" -Path "/api/usuarios/$usuarioId" -ExpectedStatus @(200) -Description "Eliminar usuario existente" | Out-Null

    # 11. Eliminar rol
    Invoke-ApiTest -Method "DELETE" -Path "/api/roles/$rolId" -ExpectedStatus @(200) -Description "Eliminar rol existente" | Out-Null

    # 12. Crear respaldo de la base de datos
    Invoke-ApiTest -Method "POST" -Path "/api/database/backup" -ExpectedStatus @(200) -Description "Crear y descargar respaldo SQLite" | Out-Null

    # 13. Vaciar base de datos
    Invoke-ApiTest -Method "DELETE" -Path "/api/database/vaciar" -ExpectedStatus @(200) -Description "Vaciar tablas de base de datos" | Out-Null

    Write-Host "`n==================================================" -ForegroundColor Green
    Write-Host " TODAS LAS PRUEBAS DE USUARIOS-API FINALIZARON CON ÉXITO" -ForegroundColor Green
    Write-Host "==================================================" -ForegroundColor Green
}
catch {
    Write-Host "`nLAS PRUEBAS SE DETUVIERON POR UN ERROR: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

<?php

namespace RPA\Tests;

use PHPUnit\Framework\TestCase;
use RPA\Controllers\RPAController;
use RPA\Services\ConfigService;
use RPA\Services\LoggerService;
use RPA\Services\ValidationService;
use RPA\Services\RateLimitService;
use RPA\Services\SessionService;
use RPA\Services\MonitorService;
use RPA\Repositories\SessionRepository;

class RPAControllerTest extends TestCase
{
    private RPAController $controller;
    private $mockSessionService;
    private $mockMonitorService;
    private $mockConfigService;
    private $mockValidationService;
    private $mockRateLimitService;
    private $mockLogger;

    protected function setUp(): void
    {
        // Criar mocks
        $this->mockSessionService = $this->createMock(\RPA\Interfaces\SessionServiceInterface::class);
        $this->mockMonitorService = $this->createMock(\RPA\Interfaces\MonitorServiceInterface::class);
        $this->mockConfigService = $this->createMock(ConfigService::class);
        $this->mockValidationService = $this->createMock(ValidationService::class);
        $this->mockRateLimitService = $this->createMock(RateLimitService::class);
        $this->mockLogger = $this->createMock(\RPA\Interfaces\LoggerInterface::class);

        // Configurar controller
        $this->controller = new RPAController(
            $this->mockSessionService,
            $this->mockMonitorService,
            $this->mockConfigService,
            $this->mockValidationService,
            $this->mockRateLimitService,
            $this->mockLogger
        );
    }

    public function testStartRPASuccess()
    {
        // Dados de teste
        $data = [
            'cpf' => '12345678901',
            'nome' => 'João da Silva'
        ];

        // Configurar mocks
        $this->mockRateLimitService
            ->expects($this->once())
            ->method('isAllowed')
            ->willReturn(true);

        $this->mockValidationService
            ->expects($this->once())
            ->method('validate')
            ->willReturn(new \RPA\Services\ValidationResult([]));

        $this->mockSessionService
            ->expects($this->once())
            ->method('create')
            ->with($data)
            ->willReturn([
                'success' => true,
                'session_id' => 'test_session_123',
                'message' => 'Sessão criada com sucesso'
            ]);

        // Executar teste
        $result = $this->controller->startRPA($data);

        // Verificar resultado
        $this->assertTrue($result['success']);
        $this->assertEquals('test_session_123', $result['session_id']);
        $this->assertEquals('Sessão criada com sucesso', $result['message']);
    }

    public function testStartRPARateLimitExceeded()
    {
        // Dados de teste
        $data = [
            'cpf' => '12345678901',
            'nome' => 'João da Silva'
        ];

        // Configurar mocks
        $this->mockRateLimitService
            ->expects($this->once())
            ->method('isAllowed')
            ->willReturn(false);

        // Executar teste
        $result = $this->controller->startRPA($data);

        // Verificar resultado
        $this->assertFalse($result['success']);
        $this->assertEquals('Rate limit exceeded. Try again later.', $result['error']);
    }

    public function testStartRPAValidationFailed()
    {
        // Dados de teste
        $data = [
            'cpf' => '123', // CPF inválido
            'nome' => 'João da Silva'
        ];

        // Configurar mocks
        $this->mockRateLimitService
            ->expects($this->once())
            ->method('isAllowed')
            ->willReturn(true);

        $this->mockValidationService
            ->expects($this->once())
            ->method('validate')
            ->willReturn(new \RPA\Services\ValidationResult(['CPF inválido']));

        // Executar teste
        $result = $this->controller->startRPA($data);

        // Verificar resultado
        $this->assertFalse($result['success']);
        $this->assertStringContains('Dados inválidos', $result['error']);
    }

    public function testGetStatusSuccess()
    {
        // Dados de teste
        $sessionId = 'test_session_123';
        $sessionData = [
            'session_id' => $sessionId,
            'status' => 'running',
            'progress' => 50
        ];

        // Configurar mocks
        $this->mockSessionService
            ->expects($this->once())
            ->method('getStatus')
            ->with($sessionId)
            ->willReturn([
                'success' => true,
                'session' => $sessionData
            ]);

        // Executar teste
        $result = $this->controller->getStatus($sessionId);

        // Verificar resultado
        $this->assertTrue($result['success']);
        $this->assertEquals($sessionData, $result['session']);
    }

    public function testGetStatusNotFound()
    {
        // Dados de teste
        $sessionId = 'nonexistent_session';

        // Configurar mocks
        $this->mockSessionService
            ->expects($this->once())
            ->method('getStatus')
            ->with($sessionId)
            ->willReturn([
                'success' => false,
                'error' => 'Sessão não encontrada'
            ]);

        // Executar teste
        $result = $this->controller->getStatus($sessionId);

        // Verificar resultado
        $this->assertFalse($result['success']);
        $this->assertEquals('Sessão não encontrada', $result['error']);
    }

    public function testListSessionsSuccess()
    {
        // Dados de teste
        $sessions = [
            [
                'session_id' => 'session_1',
                'status' => 'completed',
                'created_at' => '2025-09-30 08:00:00'
            ],
            [
                'session_id' => 'session_2',
                'status' => 'running',
                'created_at' => '2025-09-30 09:00:00'
            ]
        ];

        // Configurar mocks
        $this->mockSessionService
            ->expects($this->once())
            ->method('list')
            ->willReturn([
                'success' => true,
                'sessions' => $sessions,
                'total' => 2
            ]);

        // Executar teste
        $result = $this->controller->listSessions();

        // Verificar resultado
        $this->assertTrue($result['success']);
        $this->assertEquals($sessions, $result['sessions']);
        $this->assertEquals(2, $result['total']);
    }

    public function testHealthCheckSuccess()
    {
        // Dados de teste
        $healthData = [
            'status' => 'healthy',
            'timestamp' => '2025-09-30 10:00:00',
            'checks' => [
                'sessions' => ['status' => 'ok'],
                'data' => ['status' => 'ok']
            ]
        ];

        // Configurar mocks
        $this->mockMonitorService
            ->expects($this->once())
            ->method('healthCheck')
            ->willReturn($healthData);

        // Executar teste
        $result = $this->controller->healthCheck();

        // Verificar resultado
        $this->assertTrue($result['success']);
        $this->assertEquals($healthData, $result['health']);
    }

    public function testStopSessionSuccess()
    {
        // Dados de teste
        $sessionId = 'test_session_123';

        // Configurar mocks
        $this->mockSessionService
            ->expects($this->once())
            ->method('stop')
            ->with($sessionId)
            ->willReturn([
                'success' => true,
                'message' => 'Sessão parada com sucesso'
            ]);

        // Executar teste
        $result = $this->controller->stopSession($sessionId);

        // Verificar resultado
        $this->assertTrue($result['success']);
        $this->assertEquals('Sessão parada com sucesso', $result['message']);
    }

    public function testCleanupSuccess()
    {
        // Configurar mocks
        $this->mockSessionService
            ->expects($this->once())
            ->method('cleanup')
            ->willReturn([
                'success' => true,
                'cleaned' => 5,
                'message' => 'Limpeza concluída: 5 sessões removidas'
            ]);

        // Executar teste
        $result = $this->controller->cleanup();

        // Verificar resultado
        $this->assertTrue($result['success']);
        $this->assertEquals(5, $result['cleaned']);
    }
}

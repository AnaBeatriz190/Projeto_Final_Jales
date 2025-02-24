# Função para Inserir uma Nova Refeição

CREATE FUNCTION inserir_refeicao(nome_refeicao VARCHAR(100), data_refeicao DATE)
RETURNS VOID AS $$
BEGIN
    INSERT INTO refeicoes (nome, data)
    VALUES (nome_refeicao, data_refeicao);
END;
$$ LANGUAGE plpgsql;

# Função para Verificar Disponibilidade de Vagas
CREATE FUNCTION verificar_vagas_disponiveis(refeicao_id INT, limite_vagas INT)
RETURNS BOOLEAN AS $$
DECLARE
    total_inscricoes INT;
BEGIN
    SELECT COUNT(*) INTO total_inscricoes
    FROM inscricoes
    WHERE refeicao_id = verificar_vagas_disponiveis.refeicao_id;

    RETURN total_inscricoes < limite_vagas;
END;
$$ LANGUAGE plpgsql;
document.addEventListener('DOMContentLoaded', function() {
  // Elementos do DOM
  const valorInput = document.getElementById("valor_emprestimo");
  const bancoSelect = document.getElementById("banco");
  const prazoSelect = document.getElementById("prazo_financiamento");
  
  // Elementos de resultado
  const valorParcelaBanco = document.getElementById("valor-parcela-banco");
  const valorParcelaSicredi = document.getElementById("valor-parcela-sicredi");
  const valorTaxaBanco = document.getElementById("valor-taxa-banco");
  const valorTaxaSicredi = document.getElementById("valor-taxa-sicredi");
  const bancoNome = document.getElementById("banco-nome");
  const bancoNomeParcela = document.getElementById("banco-nome-parcela");
  const bancoNomeTotal = document.getElementById("banco-nome-total");

  // Nomes dos bancos para exibição
  const nomesBancos = {
      "0.03": "BRB",
      "0.017": "Inter",
      "0.05": "Itaú",
      "0.06": "Nubank",
      "0.07": "Santander"
  };

  // Adiciona event listeners para recalcular quando qualquer input mudar
  valorInput.addEventListener('input', calcular);
  bancoSelect.addEventListener('change', calcular);
  prazoSelect.addEventListener('change', calcular);

  function calcular() {
      const valor = parseFloat(valorInput.value);
      const taxaBanco = parseFloat(bancoSelect.value);
      const prazo = parseInt(prazoSelect.value);
      const taxaSicredi = 0.015; // 1.5% em decimal
      
      // Verifica se os valores são válidos
      if (isNaN(valor)) return;
      if (isNaN(taxaBanco)) return;
      
      // Obtém o nome do banco selecionado
      const nomeBanco = nomesBancos[bancoSelect.value] || "Banco";
      
      // Atualiza os nomes dos bancos nos textos
      bancoNome.textContent = nomeBanco;
      bancoNomeParcela.textContent = nomeBanco;
      bancoNomeTotal.textContent = nomeBanco;
      
      // Calcula as parcelas
      const parcelaSicredi = calcularParcela(valor, taxaSicredi, prazo);
      const parcelaBanco = calcularParcela(valor, taxaBanco, prazo);
      
      // Calcula os totais
      const totalSicredi = parcelaSicredi * prazo;
      const totalBanco = parcelaBanco * prazo;
      
      // Atualiza os valores na tela
      valorParcelaBanco.textContent = `R$ ${parcelaBanco.toFixed(2)}`;
      valorParcelaSicredi.textContent = `R$ ${parcelaSicredi.toFixed(2)}`;
      valorTaxaBanco.textContent = `R$ ${totalBanco.toFixed(2)}`;
      valorTaxaSicredi.textContent = `R$ ${totalSicredi.toFixed(2)}`;
  }

  function calcularParcela(pv, taxa, prazo) {
      const i = taxa; // Já está em decimal (0.03 para 3%)
      const n = prazo;
      return (pv * i) / (1 - Math.pow(1 + i, -n));
  }
});

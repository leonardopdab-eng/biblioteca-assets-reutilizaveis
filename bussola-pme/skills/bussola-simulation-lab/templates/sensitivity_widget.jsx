// sensitivity_widget.jsx — Componente React para simulação interativa Bússola PME
// Deps: recharts (npm install recharts)
// Usage: <SensitivityWidget data={simulationData} />

import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const COLORS = {
  pessimista: '#E74C3C',   // red
  realista: '#2E86AB',      // blue (Bússola PME primary)
  otimista: '#27AE60',      // green
};

const SensitivityWidget = ({ data = {} }) => {
  const [activeScenario, setActiveScenario] = useState('all');

  // Transform data for recharts
  const chartData = (data.scenarios || []).map((point) => ({
    variable: point.price || point.month || point.stage || point.x,
    pessimista: point.pessimista_revenue || point.pessimista || 0,
    realista: point.realista_revenue || point.realista || 0,
    otimista: point.otimista_revenue || point.otimista || 0,
    label: point.label || '',
  }));

  const formatCurrency = (value) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }).format(value);

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', padding: '24px', background: '#EBF5FB', borderRadius: '8px' }}>
      <h2 style={{ color: '#1B4F72', marginBottom: '8px' }}>
        {data.title || 'Análise de Sensibilidade — Bússola PME'}
      </h2>
      <p style={{ color: '#7F8C8D', fontSize: '14px', marginBottom: '16px' }}>
        {data.subtitle || 'Projeção por cenário [HIPÓTESE — validar com dados reais]'}
      </p>

      {/* Scenario toggles */}
      <div style={{ marginBottom: '16px', display: 'flex', gap: '8px' }}>
        {['all', 'pessimista', 'realista', 'otimista'].map((s) => (
          <button
            key={s}
            onClick={() => setActiveScenario(s)}
            style={{
              padding: '6px 12px',
              borderRadius: '4px',
              border: 'none',
              background: activeScenario === s ? '#1B4F72' : '#fff',
              color: activeScenario === s ? '#fff' : '#1B4F72',
              cursor: 'pointer',
              fontSize: '13px',
            }}
          >
            {s === 'all' ? 'Todos' : s.charAt(0).toUpperCase() + s.slice(1)}
          </button>
        ))}
      </div>

      {/* Chart */}
      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={chartData} margin={{ top: 5, right: 20, left: 60, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#D5E8F0" />
          <XAxis dataKey="variable" tick={{ fontSize: 12 }} />
          <YAxis tickFormatter={formatCurrency} tick={{ fontSize: 11 }} />
          <Tooltip formatter={(value) => formatCurrency(value)} />
          <Legend />
          {(activeScenario === 'all' || activeScenario === 'pessimista') && (
            <Line type="monotone" dataKey="pessimista" stroke={COLORS.pessimista}
              strokeWidth={2} dot={false} name="Pessimista" />
          )}
          {(activeScenario === 'all' || activeScenario === 'realista') && (
            <Line type="monotone" dataKey="realista" stroke={COLORS.realista}
              strokeWidth={2.5} dot={false} name="Realista" />
          )}
          {(activeScenario === 'all' || activeScenario === 'otimista') && (
            <Line type="monotone" dataKey="otimista" stroke={COLORS.otimista}
              strokeWidth={2} dot={false} name="Otimista" />
          )}
        </LineChart>
      </ResponsiveContainer>

      {/* CTA */}
      {data.cta && (
        <div style={{ marginTop: '16px', textAlign: 'center' }}>
          <button
            onClick={() => window.sendPrompt && window.sendPrompt(data.cta.prompt || 'quero saber mais')}
            style={{
              padding: '10px 24px',
              background: '#F39C12',
              color: '#fff',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: '600',
            }}
          >
            {data.cta.label || 'Ver próximos passos'}
          </button>
        </div>
      )}

      <p style={{ color: '#7F8C8D', fontSize: '12px', marginTop: '12px', textAlign: 'center' }}>
        ⚠️ Projeções baseadas em premissas [HIPÓTESE]. Validar antes de decisão.
      </p>
    </div>
  );
};

export default SensitivityWidget;

// showcase_interactive.jsx — Showcase interativo Bússola PME
// Deps: recharts (npm install recharts)
// Usage: <ShowcaseInteractive data={showcaseData} />
// showcaseData shape:
//   { case_id, segment, team_size, problema_central,
//     achados_chave: string[], top_acoes: string[],
//     metrica_destaque, resultado_esperado, cta }

import React, { useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell,
} from 'recharts';

const TOKENS = {
  primary: '#1B4F72',
  secondary: '#2E86AB',
  accent: '#F39C12',
  success: '#27AE60',
  bg: '#EBF5FB',
  card: '#FFFFFF',
  textHead: '#1B4F72',
  textBody: '#2C3E50',
  textMuted: '#7F8C8D',
  border: '#D5E8F0',
};

const styles = {
  wrapper: {
    fontFamily: 'Inter, system-ui, sans-serif',
    background: TOKENS.bg,
    minHeight: '100vh',
    padding: '0',
  },
  hero: {
    background: TOKENS.primary,
    color: '#fff',
    padding: '48px 32px',
    textAlign: 'center',
  },
  heroTitle: {
    fontSize: '28px',
    fontWeight: 700,
    marginBottom: '12px',
    color: '#fff',
  },
  heroSub: {
    fontSize: '16px',
    color: '#AED6F1',
    maxWidth: '600px',
    margin: '0 auto 24px',
  },
  ctaBtn: {
    background: TOKENS.accent,
    color: '#fff',
    border: 'none',
    borderRadius: '6px',
    padding: '12px 28px',
    fontSize: '15px',
    fontWeight: 600,
    cursor: 'pointer',
  },
  section: {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '32px 24px',
  },
  sectionTitle: {
    fontSize: '20px',
    fontWeight: 700,
    color: TOKENS.textHead,
    marginBottom: '16px',
    borderLeft: `4px solid ${TOKENS.accent}`,
    paddingLeft: '12px',
  },
  card: {
    background: TOKENS.card,
    borderRadius: '8px',
    padding: '20px',
    marginBottom: '16px',
    boxShadow: '0 2px 8px rgba(27,79,114,0.10)',
  },
  badge: {
    display: 'inline-block',
    background: TOKENS.bg,
    border: `1px solid ${TOKENS.border}`,
    borderRadius: '4px',
    padding: '3px 8px',
    fontSize: '12px',
    color: TOKENS.primary,
    marginRight: '6px',
  },
  disclaimer: {
    color: TOKENS.textMuted,
    fontSize: '12px',
    textAlign: 'center',
    marginTop: '8px',
  },
};

const PhaseBar = ({ phase, label, active }) => (
  <div style={{
    padding: '10px 14px',
    borderRadius: '6px',
    background: active ? TOKENS.primary : TOKENS.card,
    color: active ? '#fff' : TOKENS.textBody,
    border: `1px solid ${TOKENS.border}`,
    fontSize: '13px',
    fontWeight: active ? 600 : 400,
    marginBottom: '6px',
    display: 'flex',
    gap: '10px',
    alignItems: 'center',
  }}>
    <span style={{
      width: '22px', height: '22px', borderRadius: '50%',
      background: active ? TOKENS.accent : TOKENS.border,
      color: active ? '#fff' : TOKENS.textMuted,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontSize: '12px', fontWeight: 700, flexShrink: 0,
    }}>{phase}</span>
    {label}
  </div>
);

const ShowcaseInteractive = ({ data = {} }) => {
  const [activePhase, setActivePhase] = useState(4);

  const {
    segment = 'Agência B2B de comunicação',
    team_size = '5–10 pessoas',
    problema_central = 'Pipeline em queda constante sem causa raiz identificada.',
    achados_chave = [
      'Prospecção sem cadência definida',
      'Taxa de conversão em queda por falta de qualificação',
      'Tempo de resposta ao lead acima de 48h',
    ],
    top_acoes = [
      'Cadência semanal de prospecção com script por ICP',
      'Qualificação BANT antes de envio de proposta',
      'SLA de resposta ao lead reduzido para < 4h',
    ],
    metrica_destaque = '~40–50% de melhoria no pipeline',
    cta = {},
  } = data;

  const phases = [
    'Configuração', 'Intake', 'Normalização',
    'Diagnóstico', 'Priorização', 'Plano de Ação',
  ];

  const chartData = [
    { name: 'Antes', value: 60, fill: '#E74C3C' },
    { name: 'Depois', value: 95, fill: TOKENS.success },
  ];

  return (
    <div style={styles.wrapper}>
      {/* HERO */}
      <div style={styles.hero}>
        <div style={{ fontSize: '13px', color: '#AED6F1', marginBottom: '8px' }}>
          Bússola PME — Case Showcase
        </div>
        <h1 style={styles.heroTitle}>
          Como uma {segment} com {team_size} recuperou o crescimento
        </h1>
        <p style={styles.heroSub}>
          Diagnóstico estruturado. Priorização com dados. Plano de ação com owner e prazo.
        </p>
        <button
          style={styles.ctaBtn}
          onClick={() => cta.prompt && window.sendPrompt?.(cta.prompt)}
        >
          {cta.label || 'Quero meu diagnóstico gratuito'}
        </button>
      </div>

      {/* SITUAÇÃO */}
      <div style={styles.section}>
        <div style={styles.sectionTitle}>O Problema</div>
        <div style={styles.card}>
          <p style={{ color: TOKENS.textBody, lineHeight: '1.6', margin: 0 }}>
            {problema_central}
          </p>
        </div>

        {/* ACHADOS */}
        <div style={styles.sectionTitle}>3 Achados do Diagnóstico</div>
        {achados_chave.map((achado, i) => (
          <div key={i} style={{ ...styles.card, display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
            <span style={{
              width: '28px', height: '28px', borderRadius: '50%',
              background: TOKENS.accent, color: '#fff',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '13px', fontWeight: 700, flexShrink: 0,
            }}>{i + 1}</span>
            <span style={{ color: TOKENS.textBody, lineHeight: '1.5' }}>{achado}</span>
          </div>
        ))}

        {/* MÉTODO */}
        <div style={styles.sectionTitle}>O Método em 6 Fases</div>
        <div style={styles.card}>
          {phases.map((label, i) => (
            <div key={i} onClick={() => setActivePhase(i + 1)} style={{ cursor: 'pointer' }}>
              <PhaseBar phase={i + 1} label={label} active={activePhase === i + 1} />
            </div>
          ))}
          <p style={{ ...styles.disclaimer, marginTop: '12px' }}>
            Clique em cada fase para destacá-la
          </p>
        </div>

        {/* AÇÕES */}
        <div style={styles.sectionTitle}>Top 3 Ações Implementadas</div>
        {top_acoes.map((acao, i) => (
          <div key={i} style={{ ...styles.card, borderLeft: `3px solid ${TOKENS.secondary}` }}>
            <span style={styles.badge}>Ação {i + 1}</span>
            <span style={{ color: TOKENS.textBody, fontSize: '14px' }}>{acao}</span>
          </div>
        ))}

        {/* RESULTADO */}
        <div style={styles.sectionTitle}>Resultado</div>
        <div style={{ ...styles.card, textAlign: 'center' }}>
          <div style={{ fontSize: '32px', fontWeight: 700, color: TOKENS.success, marginBottom: '8px' }}>
            {metrica_destaque}
          </div>
          <p style={{ color: TOKENS.textMuted, fontSize: '13px', margin: 0 }}>
            Métrica arredondada para faixa ±5% [CASO REAL — dados aproximados]
          </p>
        </div>

        {/* MINI CHART */}
        <div style={styles.card}>
          <div style={{ fontWeight: 600, color: TOKENS.textHead, marginBottom: '12px' }}>
            Comparativo Antes × Depois
          </div>
          <ResponsiveContainer width="100%" height={160}>
            <BarChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke={TOKENS.border} />
              <XAxis dataKey="name" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 11 }} domain={[0, 100]} unit="%" />
              <Tooltip formatter={(v) => `~${v}%`} />
              <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                {chartData.map((entry, i) => (
                  <Cell key={i} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <p style={styles.disclaimer}>
            ⚠️ Valores ilustrativos arredondados. [HIPÓTESE — validar com dados reais]
          </p>
        </div>

        {/* CTA FINAL */}
        <div style={{ ...styles.card, textAlign: 'center', background: TOKENS.primary }}>
          <h3 style={{ color: '#fff', marginBottom: '8px' }}>
            Sua empresa também pode ter esse diagnóstico
          </h3>
          <p style={{ color: '#AED6F1', fontSize: '14px', marginBottom: '16px' }}>
            Sessão de 60 minutos, sem compromisso
          </p>
          <button
            style={styles.ctaBtn}
            onClick={() => cta.prompt && window.sendPrompt?.(cta.prompt)}
          >
            {cta.label || 'Agendar diagnóstico gratuito'}
          </button>
        </div>

        <p style={{ ...styles.disclaimer, marginTop: '24px' }}>
          Bússola PME — Dados anonimizados. Resultados reais variam por contexto e segmento.
        </p>
      </div>
    </div>
  );
};

export default ShowcaseInteractive;

import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine,
} from 'recharts'

export function NDVIChart({ observations }) {
  const data = observations.map(o => ({
    date: o.obs_date.slice(5), // MM-DD
    ndvi: +o.ndvi_mean.toFixed(3),
    evi: +o.evi_mean.toFixed(3),
  }))

  return (
    <ResponsiveContainer width="100%" height={200}>
      <LineChart data={data} margin={{ top: 8, right: 12, bottom: 0, left: -10 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#30363d" />
        <XAxis dataKey="date" tick={{ fill: '#8b949e', fontSize: 11 }} />
        <YAxis domain={[0, 1]} tick={{ fill: '#8b949e', fontSize: 11 }} />
        <Tooltip
          contentStyle={{ background: '#1c2128', border: '1px solid #30363d', borderRadius: 6 }}
          labelStyle={{ color: '#e6edf3' }}
        />
        <ReferenceLine y={0.4} stroke="#f85149" strokeDasharray="4 4" label={{ value: 'crítico', fill: '#f85149', fontSize: 10 }} />
        <Line type="monotone" dataKey="ndvi" stroke="#3fb950" strokeWidth={2} dot={{ r: 3 }} name="NDVI" />
        <Line type="monotone" dataKey="evi" stroke="#58a6ff" strokeWidth={1.5} dot={false} name="EVI" strokeDasharray="4 2" />
      </LineChart>
    </ResponsiveContainer>
  )
}

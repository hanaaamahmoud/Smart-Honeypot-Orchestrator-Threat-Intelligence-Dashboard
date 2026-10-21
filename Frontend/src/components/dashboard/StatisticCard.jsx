function StatisticCard({
  title,
  value,
  subtitle,
  icon,
  variant = "blue",
}) {
  return (
    <article
      className={`stat-card stat-card-${variant}`}
    >
      <div className="stat-card-top">
        <div className="stat-card-icon">
          {icon}
        </div>
      </div>

      <div className="stat-card-content">
        <span className="stat-card-title">
          {title}
        </span>

        <strong className="stat-card-value">
          {value}
        </strong>

        <span className="stat-card-subtitle">
          {subtitle}
        </span>
      </div>
    </article>
  );
}

export default StatisticCard;
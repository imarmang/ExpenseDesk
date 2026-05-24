import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSun, faMoon } from '@fortawesome/free-solid-svg-icons'

type Props = {
  theme: 'light' | 'dark'
  onToggleTheme: () => void
}

export default function TopBar({ theme, onToggleTheme }: Props) {
  const isDark = theme === 'dark'

  return (
    <header className="topbar">
      <div className="topbar__left">
        <div className="topbar__dot" />
        <div>
          <h1 className="topbar__name">ExpenseDesk</h1>
          <p className="topbar__sub">AI-powered expense assistant</p>
        </div>
      </div>

      <div className="topbar__right">
          <span className="topbar__theme-label">
          {isDark ? 'Dark' : 'Light'}
        </span>
        <button
          className={`topbar__toggle ${isDark ? 'topbar__toggle--active' : ''}`}
          onClick={onToggleTheme}
          aria-label="Toggle theme"
        >
        <div className="topbar__knob" />
        </button>
          <FontAwesomeIcon
          icon={isDark ? faMoon : faSun}
          className="topbar__theme-icon"
        />

      </div>
    </header>
  )
}
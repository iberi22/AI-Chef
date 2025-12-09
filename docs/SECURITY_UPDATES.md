# Security Updates - December 2025

## Vulnerabilities Fixed

### Date: December 9, 2025

#### CVE-2025-64718 (js-yaml) - Moderate Severity

- **Package**: js-yaml
- **Previous Version**: < 3.14.2
- **Fixed Version**: 3.14.2
- **Issue**: Prototype pollution in YAML merge (`<<`) operator
- **Impact**: Moderate
- **Resolution**: Updated dependency via `npm update`

#### CVE-2025-64756 (glob) - High Severity

- **Package**: glob
- **Previous Version**: >= 10.2.0, < 10.5.0
- **Fixed Version**: 10.5.0
- **Impact**: High
- **Resolution**: Updated dependency via `npm update`

## Verification

Audit completed on December 9, 2025:

```bash
npm audit
# Result: found 0 vulnerabilities
```

## Automated Security

This repository uses:

- **Dependabot**: Automated dependency updates with security alerts
- **GitHub Security Advisories**: Monitors for known vulnerabilities
- **Auto-merge workflow**: PRs labeled `automation` are auto-approved when checks pass

## Security Policy

1. All security updates are applied within 48 hours of disclosure
2. Critical vulnerabilities are addressed immediately
3. Dependencies are reviewed quarterly
4. Security audit runs on every PR

## Related PRs

- #31: Automated Dependabot PR for js-yaml updates (merged Dec 9, 2025)

## Next Steps

- Continue monitoring Dependabot alerts
- Regular dependency updates via `npm update`
- Consider implementing npm audit in CI/CD pipeline

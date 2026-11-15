# NavigationRail

Leading-edge navigation for medium and larger windows (600dp and up), with the same destinations as the navigation bar.

**Provide:** `items` (`[{icon, label, badge?}]`), `value` + `onChange` (or `defaultValue`), optional `fab` (`{icon, label, onClick}`), `expanded` + `onExpandedChange` (or `defaultExpanded`), `menu={false}` to hide the expand button, `label`.

- Collapsed (96px): a menu button, the FAB, then destinations as a 56×32 pill with the label underneath. Expanded (240px): the FAB grows a label and destinations become full-width 56px rows.
- Width, pills and the FAB move on `spatial-default`; colours change on `effects-default`.
- The active destination gets `primary-container`, a filled icon and a bold label, matching the navigation bar.
- Switch from `NavigationBar` to the rail at 600dp, and expand it by default from 1200dp. Keep the same order and labels in both.

**Compose:** `WideNavigationRail` (collapsed and expanded states, material3 1.4+) or `NavigationRail`.

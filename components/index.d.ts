import type * as React from 'react';

/** A Material Symbols Rounded ligature name, e.g. "arrow_back", "add", "photo_camera". */
export type IconName = string;
export type ShapeName = 'circle' | 'cookie4' | 'cookie6' | 'cookie9' | 'cookie12' | 'clover4' | 'flower5' | 'flower8' | 'sunny' | 'burst' | 'pebble';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> { variant?: 'filled' | 'tonal' | 'outlined' | 'text' | 'elevated'; size?: 'sm' | 'md' | 'lg'; tone?: 'error' | 'ink'; icon?: IconName; fullWidth?: boolean }
export declare function Button(props: ButtonProps): React.ReactElement;

export interface IconButtonProps { icon: IconName; label: string; variant?: 'standard' | 'filled' | 'tonal' | 'outlined'; selected?: boolean; size?: 'sm'; onClick?: () => void; disabled?: boolean; className?: string }
export declare function IconButton(props: IconButtonProps): React.ReactElement;

export interface FabProps { icon: IconName; label?: string; ariaLabel?: string; tone?: 'primary' | 'highlight' | 'secondary' | 'surface'; size?: 'md' | 'lg'; onClick?: () => void; className?: string }
export declare function Fab(props: FabProps): React.ReactElement;

export interface ButtonGroupOption { value: string; label: string; icon?: IconName; sub?: string }
export interface ButtonGroupProps { options: ButtonGroupOption[]; value?: string; defaultValue?: string; onChange?: (value: string) => void; label?: string; tone?: 'secondary' | 'container'; fit?: boolean; className?: string }
export declare function ButtonGroup(props: ButtonGroupProps): React.ReactElement;

export interface ChipProps { label: string; icon?: IconName; count?: number | string; selected?: boolean; defaultSelected?: boolean; variant?: 'outlined' | 'tonal'; onClick?: (selected: boolean) => void; className?: string }
export declare function Chip(props: ChipProps): React.ReactElement;

export interface BadgeProps { children?: React.ReactNode; tone?: 'primary' | 'tertiary' | 'positive' | 'error' | 'highlight'; mono?: boolean; dot?: boolean; count?: number | string; className?: string }
export declare function Badge(props: BadgeProps): React.ReactElement;

export interface ValuePillProps { children: React.ReactNode; direction?: 'up' | 'down'; solid?: boolean; inline?: boolean }
export declare function ValuePill(props: ValuePillProps): React.ReactElement;

export interface NavItem { icon: IconName; label: string; badge?: number }
export interface NavigationBarProps { items: NavItem[]; value?: number; defaultValue?: number; onChange?: (index: number) => void; label?: string; className?: string }
export declare function NavigationBar(props: NavigationBarProps): React.ReactElement;

export interface TopBarAction { icon: IconName; label: string; onClick?: () => void; selected?: boolean }
export interface TopBarProps { title: React.ReactNode; subtitle?: React.ReactNode; eyebrow?: string; leading?: 'back' | 'close'; onLeading?: () => void; actions?: TopBarAction[]; size?: 'small' | 'large'; display?: boolean }
export declare function TopBar(props: TopBarProps): React.ReactElement;

export interface SearchBarProps { placeholder?: string; defaultValue?: string; onChange?: (value: string) => void; icon?: IconName; trailing?: React.ReactNode; id?: string; className?: string }
export declare function SearchBar(props: SearchBarProps): React.ReactElement;

export interface TextFieldProps { label?: string; defaultValue?: string; placeholder?: string; supportingText?: string; error?: string; multiline?: boolean; variant?: 'outlined' | 'filled'; trailingIcon?: IconName; inputMode?: React.HTMLAttributes<HTMLInputElement>['inputMode']; onChange?: (value: string) => void; id?: string; className?: string }
export declare function TextField(props: TextFieldProps): React.ReactElement;

export interface SwitchProps { label?: string | null; supportingText?: string; checked?: boolean; defaultChecked?: boolean; onChange?: (checked: boolean) => void }
export declare function Switch(props: SwitchProps): React.ReactElement;

export interface SliderProps { label?: string; value?: number; defaultValue?: number; onChange?: (value: number) => void; min?: number; max?: number; step?: number; format?: (value: number) => React.ReactNode; supportingText?: string; id?: string }
export declare function Slider(props: SliderProps): React.ReactElement;

export interface WavyProgressProps { value: number; label?: string; animated?: boolean; flat?: boolean }
export declare function WavyProgress(props: WavyProgressProps): React.ReactElement;

export interface CardProps { children?: React.ReactNode; title?: React.ReactNode; body?: React.ReactNode; eyebrow?: string; variant?: 'low' | 'filled' | 'outlined' | 'elevated' | 'primary' | 'secondary' | 'tertiary' | 'highlight'; padding?: 'sm'; display?: boolean; onClick?: () => void; className?: string; style?: React.CSSProperties }
export declare function Card(props: CardProps): React.ReactElement;

export interface ListItemProps { headline: React.ReactNode; supporting?: React.ReactNode; meta?: React.ReactNode; leading?: React.ReactNode; trailing?: React.ReactNode; onClick?: () => void; className?: string }
export declare function ListItem(props: ListItemProps): React.ReactElement;

export interface GroupedListProps { title?: string; children: React.ReactNode }
export declare function GroupedList(props: GroupedListProps): React.ReactElement;

export interface StatTileProps { value: React.ReactNode; label: React.ReactNode; tone?: 'primary' | 'primary-container' | 'positive' | 'tertiary'; display?: boolean }
export declare function StatTile(props: StatTileProps): React.ReactElement;

export interface ShapeAvatarProps { shape?: ShapeName; text?: string; icon?: IconName; tone?: 'primary' | 'primary-container' | 'secondary' | 'secondary-container' | 'tertiary-container' | 'highlight' | 'positive'; size?: number; label?: string; spin?: boolean; className?: string }
export declare const ShapeAvatar: ((props: ShapeAvatarProps) => React.ReactElement) & { shapes: ShapeName[]; path: (name: ShapeName) => string };

export interface BottomSheetProps { title?: string; subtitle?: string; eyebrow?: string; eyebrowTone?: BadgeProps['tone']; children?: React.ReactNode }
export declare function BottomSheet(props: BottomSheetProps): React.ReactElement;

export interface SummaryRow { label: React.ReactNode; value: React.ReactNode; tone?: 'positive' | 'error'; total?: boolean }
export interface SummaryListProps { rows: SummaryRow[]; footnote?: React.ReactNode }
export declare function SummaryList(props: SummaryListProps): React.ReactElement;

export interface SnackbarProps { message: string; action?: string; onAction?: () => void }
export declare function Snackbar(props: SnackbarProps): React.ReactElement;

export interface LoadingIndicatorProps { size?: number; contained?: boolean; label?: string }
export declare function LoadingIndicator(props: LoadingIndicatorProps): React.ReactElement;

export interface SplitButtonItem { label: string; icon?: IconName; onClick?: () => void }
export interface SplitButtonProps { children: React.ReactNode; icon?: IconName; variant?: 'filled' | 'tonal' | 'outlined'; size?: 'sm' | 'md'; items?: SplitButtonItem[]; menuLabel?: string; defaultOpen?: boolean; onClick?: () => void }
export declare function SplitButton(props: SplitButtonProps): React.ReactElement;

export interface ToolbarItem { icon: IconName; label: string; toggle?: boolean; onClick?: () => void }
export interface FloatingToolbarProps { items: ToolbarItem[]; value?: number; defaultValue?: number; vibrant?: boolean; label?: string; fab?: FabProps }
export declare function FloatingToolbar(props: FloatingToolbarProps): React.ReactElement;

declare global { interface Window { Expressive: { Button: typeof Button; IconButton: typeof IconButton; Fab: typeof Fab; ButtonGroup: typeof ButtonGroup; Chip: typeof Chip; Badge: typeof Badge; ValuePill: typeof ValuePill; NavigationBar: typeof NavigationBar; TopBar: typeof TopBar; SearchBar: typeof SearchBar; TextField: typeof TextField; Switch: typeof Switch; Slider: typeof Slider; WavyProgress: typeof WavyProgress; Card: typeof Card; ListItem: typeof ListItem; GroupedList: typeof GroupedList; StatTile: typeof StatTile; ShapeAvatar: typeof ShapeAvatar; BottomSheet: typeof BottomSheet; SummaryList: typeof SummaryList; Snackbar: typeof Snackbar; LoadingIndicator: typeof LoadingIndicator; SplitButton: typeof SplitButton; FloatingToolbar: typeof FloatingToolbar } } }

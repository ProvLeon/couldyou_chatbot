// frontend/components/LanguageSelector.tsx
interface LanguageSelectorProps {
  value: string;
  onChange: (language: string) => void;
}

export const LanguageSelector = (
  { value, onChange }: LanguageSelectorProps,
) => {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="px-3 py-1 rounded border focus:outline-none focus:ring-2 focus:ring-purple-400"
    >
      <option value="en">English</option>
      <option value="fr">Français</option>
    </select>
  );
};

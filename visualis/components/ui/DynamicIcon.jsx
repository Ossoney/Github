import dynamic from 'next/dynamic'
import { HelpCircle } from 'lucide-react'

// Map of all available icons in lucide-react
// We import this dynamically from the library itself if possible, 
// OR we rely on next/dynamic to handle the chunking.
import dynamicIconImports from 'lucide-react/dynamicIconImports'

const IconLoading = () => <div className="w-5 h-5 bg-slate-800/50 rounded animate-pulse" />

// Cache for created components to avoid recreation on re-render
const iconCache = {}

export const DynamicIcon = ({ name, ...props }) => {
    // Fallback if name is missing or invalid
    if (!name || !dynamicIconImports[name]) {
        return <HelpCircle {...props} />
    }

    // Return cached component if exists
    if (!iconCache[name]) {
        iconCache[name] = dynamic(dynamicIconImports[name], {
            loading: IconLoading,
            ssr: false // Icons usually client-side only for this app context
        })
    }

    const Icon = iconCache[name]
    return <Icon {...props} />
}

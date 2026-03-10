import { useState, useEffect } from 'react'
import { Card } from '@/components/ui/UI'
import { X, Delete } from 'lucide-react'
import { cn } from '@/lib/utils'

export function CalculatorModal({ isOpen, onClose, onConfirm, initialValue = '0' }) {
    const [expression, setExpression] = useState(initialValue || '0')
    const [result, setResult] = useState(initialValue || '0')

    useEffect(() => {
        if (isOpen) {
            setExpression(initialValue || '0')
            setResult(initialValue || '0')
        }
    }, [isOpen, initialValue])

    if (!isOpen) return null

    const handlePress = (val) => {
        if (expression === '0' && val !== '.' && !['+', '-', '*', '/'].includes(val)) {
            setExpression(val)
        } else {
            setExpression(prev => prev + val)
        }
    }

    const calculateResult = (expr) => {
        try {
            // Evaluates simple math safely without eval if possible, but eval is easiest for basic arithmetic.
            // Replace visual operators if any
            let cleanExpr = expr.replace(/×/g, '*').replace(/÷/g, '/')
            // Safe evaluation using Function
            const res = new Function('return ' + cleanExpr)()
            return Number.isFinite(res) ? res.toString() : 'Error'
        } catch {
            return 'Error'
        }
    }

    const handleEquals = () => {
        const res = calculateResult(expression)
        if (res !== 'Error') {
            setExpression(res)
            setResult(res)
            // Optional: automatically confirm on equals
        }
    }

    const handleDelete = () => {
        setExpression(prev => {
            if (prev.length <= 1) return '0'
            return prev.slice(0, -1)
        })
    }

    const handleClear = () => {
        setExpression('0')
        setResult('0')
    }

    const handleConfirm = () => {
        const res = calculateResult(expression)
        if (res !== 'Error') {
            onConfirm(res)
        }
    }

    const buttons = [
        ['C', '÷', '×', 'DEL'],
        ['7', '8', '9', '-'],
        ['4', '5', '6', '+'],
        ['1', '2', '3', '='],
        ['0', '.', '']
    ]

    return (
        <div className="fixed inset-0 z-[60] flex items-end sm:items-center justify-center bg-black/80 backdrop-blur-sm p-2 sm:p-4 animate-in fade-in duration-200">
            <Card className="w-full max-w-sm bg-slate-900 border-slate-800 shadow-2xl animate-in slide-in-from-bottom-10 flex flex-col overflow-hidden rounded-3xl">

                {/* Header */}
                <div className="p-4 flex justify-between items-center border-b border-slate-800">
                    <span className="text-sm font-medium text-slate-400">Calculadora</span>
                    <button onClick={onClose} className="p-2 -mr-2 text-slate-500 hover:text-slate-300 rounded-full hover:bg-slate-800 transition-colors">
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Display */}
                <div className="p-6 bg-slate-950 flex flex-col items-end gap-2">
                    <div className="text-slate-500 text-lg h-7 font-mono tracking-wider overflow-hidden max-w-full truncate">
                        {expression !== result ? expression : ''}
                    </div>
                    <div className="text-4xl font-bold text-slate-100 font-mono tracking-tight overflow-hidden max-w-full truncate">
                        {calculateResult(expression) === 'Error' ? expression : calculateResult(expression)}
                    </div>
                </div>

                {/* Keypad */}
                <div className="p-2 gap-2 grid grid-cols-4 bg-slate-900">
                    {/* Row 1 */}
                    <button onClick={handleClear} className="p-4 text-xl font-medium text-rose-400 bg-slate-800/50 hover:bg-slate-800 rounded-2xl active:scale-95 transition-all">C</button>
                    <button onClick={() => handlePress('/')} className="p-4 text-xl font-medium text-sky-400 bg-slate-800/50 hover:bg-slate-800 rounded-2xl active:scale-95 transition-all">÷</button>
                    <button onClick={() => handlePress('*')} className="p-4 text-xl font-medium text-sky-400 bg-slate-800/50 hover:bg-slate-800 rounded-2xl active:scale-95 transition-all">×</button>
                    <button onClick={handleDelete} className="p-4 flex justify-center items-center text-amber-400 bg-slate-800/50 hover:bg-slate-800 rounded-2xl active:scale-95 transition-all">
                        <Delete className="w-6 h-6" />
                    </button>

                    {/* Row 2 */}
                    <button onClick={() => handlePress('7')} className="p-4 text-2xl font-medium text-slate-200 bg-slate-800 hover:bg-slate-700 rounded-2xl active:scale-95 transition-all shadow-sm">7</button>
                    <button onClick={() => handlePress('8')} className="p-4 text-2xl font-medium text-slate-200 bg-slate-800 hover:bg-slate-700 rounded-2xl active:scale-95 transition-all shadow-sm">8</button>
                    <button onClick={() => handlePress('9')} className="p-4 text-2xl font-medium text-slate-200 bg-slate-800 hover:bg-slate-700 rounded-2xl active:scale-95 transition-all shadow-sm">9</button>
                    <button onClick={() => handlePress('-')} className="p-4 text-3xl font-medium text-sky-400 bg-slate-800/50 hover:bg-slate-800 rounded-2xl active:scale-95 transition-all">-</button>

                    {/* Row 3 */}
                    <button onClick={() => handlePress('4')} className="p-4 text-2xl font-medium text-slate-200 bg-slate-800 hover:bg-slate-700 rounded-2xl active:scale-95 transition-all shadow-sm">4</button>
                    <button onClick={() => handlePress('5')} className="p-4 text-2xl font-medium text-slate-200 bg-slate-800 hover:bg-slate-700 rounded-2xl active:scale-95 transition-all shadow-sm">5</button>
                    <button onClick={() => handlePress('6')} className="p-4 text-2xl font-medium text-slate-200 bg-slate-800 hover:bg-slate-700 rounded-2xl active:scale-95 transition-all shadow-sm">6</button>
                    <button onClick={() => handlePress('+')} className="p-4 text-3xl font-medium text-sky-400 bg-slate-800/50 hover:bg-slate-800 rounded-2xl active:scale-95 transition-all">+</button>

                    {/* Row 4 & 5 merged layout */}
                    <button onClick={() => handlePress('1')} className="p-4 text-2xl font-medium text-slate-200 bg-slate-800 hover:bg-slate-700 rounded-2xl active:scale-95 transition-all shadow-sm">1</button>
                    <button onClick={() => handlePress('2')} className="p-4 text-2xl font-medium text-slate-200 bg-slate-800 hover:bg-slate-700 rounded-2xl active:scale-95 transition-all shadow-sm">2</button>
                    <button onClick={() => handlePress('3')} className="p-4 text-2xl font-medium text-slate-200 bg-slate-800 hover:bg-slate-700 rounded-2xl active:scale-95 transition-all shadow-sm">3</button>
                    <button onClick={handleEquals} className="row-span-2 p-4 text-3xl font-medium text-white bg-sky-600 hover:bg-sky-500 rounded-2xl active:scale-95 transition-all shadow-lg shadow-sky-500/20 flex items-center justify-center">=</button>

                    <button onClick={() => handlePress('0')} className="col-span-2 p-4 text-2xl font-medium text-slate-200 bg-slate-800 hover:bg-slate-700 rounded-2xl active:scale-95 transition-all shadow-sm">0</button>
                    <button onClick={() => handlePress('.')} className="p-4 text-3xl font-medium text-slate-200 bg-slate-800 hover:bg-slate-700 rounded-2xl active:scale-95 transition-all shadow-sm">.</button>
                </div>

                {/* Confirm Area */}
                <div className="p-4 bg-slate-900 border-t border-slate-800">
                    <button
                        onClick={handleConfirm}
                        className="w-full py-4 bg-emerald-500 hover:bg-emerald-400 text-white font-bold rounded-2xl text-lg shadow-lg shadow-emerald-500/20 active:scale-[0.98] transition-all"
                    >
                        Confirmar Importe
                    </button>
                </div>

            </Card>
        </div>
    )
}

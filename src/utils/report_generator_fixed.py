import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
import json

class EnhancedReportGenerator:
    def __init__(self):
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)
        (self.reports_dir / "csv").mkdir(exist_ok=True)
        (self.reports_dir / "plots").mkdir(exist_ok=True)
        
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (16, 10)
        plt.rcParams['font.size'] = 11

    def generate_comprehensive_report(self, results: List[Any], problem_set: str):
        """Main entry point with direct strategy/model mapping"""
        print(f" Generating analysis for {problem_set}...")
        
        # Convert results with direct mapping
        df = self._create_proper_dataframe(results, problem_set)
        
        if df.empty:
            print(" No data to analyze!")
            return
        
        print(f" Created DataFrame with {len(df)} records")
        print(f"   Models: {list(df['model'].unique())}")
        print(f"   Strategies: {list(df['strategy'].unique())}")
        
        # Generate visualizations and analysis
        self._generate_performance_graphs(df, problem_set)
        self._generate_statistical_summary(df, problem_set)
        self._save_data(df, problem_set)
        
        print(f" Analysis complete!")

    def _create_proper_dataframe(self, results: List[Any], problem_set: str) -> pd.DataFrame:
        """Create DataFrame with proper strategy and model names based on expected pattern"""
        
        # Your expected configuration
        strategies = ['zero_shot', 'cot', 'few_shot', 'persona', 'template']  
        models = ['local-stub', 'starcoder-1b', 'codet5-small']
        
        print(f" Processing {len(results)} results...")
        print(f"   Expected pattern: {len(strategies)} strategies  {len(models)} models = {len(strategies) * len(models)} results")
        
        data = []
        
        # Map results to strategy/model combinations
        # Pattern: For each strategy, test all models
        result_index = 0
        
        for strategy in strategies:
            for model in models:
                if result_index < len(results):
                    result = results[result_index]
                    
                    # Extract execution time
                    exec_time = 0.0
                    for attr in ['execution_time', 'time_s', 'duration', 'elapsed_time']:
                        if hasattr(result, attr):
                            exec_time = float(getattr(result, attr, 0.0))
                            break
                    
                    # Extract success status
                    success = True
                    for attr in ['success', 'is_success', 'passed']:
                        if hasattr(result, attr):
                            success = bool(getattr(result, attr, True))
                            break
                    
                    # Extract generated code for token counting
                    generated_code = ""
                    for attr in ['generated_code', 'code', 'output', 'response']:
                        if hasattr(result, attr):
                            generated_code = str(getattr(result, attr, ""))
                            if generated_code:
                                break
                    
                    # Count tokens
                    tokens = len(generated_code.split()) if generated_code else 50
                    
                    # Extract error message
                    error_msg = ""
                    for attr in ['error_message', 'error', 'exception']:
                        if hasattr(result, attr):
                            error_msg = str(getattr(result, attr, ""))
                            break
                    
                    data.append({
                        'problem': problem_set,
                        'model': model,
                        'strategy': strategy,
                        'success': success,
                        'time_s': exec_time,
                        'tokens': tokens,
                        'error_message': error_msg,
                        'efficiency_score': self._calculate_efficiency(exec_time, tokens)
                    })
                    
                    result_index += 1
                else:
                    print(f" Missing result for {strategy} + {model}")
        
        df = pd.DataFrame(data)
        return df

    def _calculate_efficiency(self, time_s: float, tokens: int) -> float:
        """Calculate efficiency score"""
        if not time_s or time_s <= 0:
            return 0.0
        return min(10000, 1000 / (time_s * max(1, tokens/50)))

    def _generate_performance_graphs(self, df: pd.DataFrame, problem_set: str):
        """Generate clear performance graphs"""
        
        fig, axes = plt.subplots(2, 2, figsize=(18, 12))
        fig.suptitle(f'Performance Analysis: {problem_set.title()}', fontsize=16, fontweight='bold')
        
        # Strategy colors
        strategy_colors = {
            'zero_shot': '#FF6B6B', 'cot': '#4ECDC4', 'few_shot': '#45B7D1',
            'persona': '#96CEB4', 'template': '#FFEAA7'
        }
        
        # Model colors  
        model_colors = {
            'local-stub': '#FF4500', 'starcoder-1b': '#32CD32', 'codet5-small': '#4169E1'
        }
        
        # 1. Strategy Performance
        ax1 = axes[0, 0]
        strategy_avg = df.groupby('strategy')['time_s'].mean().sort_values()
        colors = [strategy_colors.get(s, '#888888') for s in strategy_avg.index]
        bars1 = ax1.bar(range(len(strategy_avg)), strategy_avg.values, color=colors, alpha=0.8)
        
        ax1.set_title('Strategy Performance Comparison', fontweight='bold')
        ax1.set_xlabel('Strategy')
        ax1.set_ylabel('Average Time (seconds)')
        ax1.set_xticks(range(len(strategy_avg)))
        ax1.set_xticklabels([s.replace('_', ' ').title() for s in strategy_avg.index], rotation=45)
        
        # Add value labels
        for bar, value in zip(bars1, strategy_avg.values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.05,
                    f'{value:.4f}s', ha='center', fontweight='bold')
        
        # 2. Model Performance  
        ax2 = axes[0, 1]
        model_avg = df.groupby('model')['time_s'].mean().sort_values()
        colors = [model_colors.get(m, '#888888') for m in model_avg.index]
        bars2 = ax2.bar(range(len(model_avg)), model_avg.values, color=colors, alpha=0.8)
        
        ax2.set_title('Model Performance Comparison', fontweight='bold')
        ax2.set_xlabel('Model')
        ax2.set_ylabel('Average Time (seconds)')
        ax2.set_xticks(range(len(model_avg)))
        ax2.set_xticklabels([m.replace('-', ' ').title() for m in model_avg.index], rotation=15)
        
        for bar, value in zip(bars2, model_avg.values):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.05,
                    f'{value:.4f}s', ha='center', fontweight='bold')
        
        # 3. Token Efficiency
        ax3 = axes[1, 0]
        token_avg = df.groupby('strategy')['tokens'].mean()
        bars3 = ax3.bar(range(len(token_avg)), token_avg.values, color='lightcoral', alpha=0.8)
        
        ax3.set_title('Token Efficiency by Strategy', fontweight='bold')
        ax3.set_xlabel('Strategy')
        ax3.set_ylabel('Average Tokens')
        ax3.set_xticks(range(len(token_avg)))
        ax3.set_xticklabels([s.replace('_', ' ').title() for s in token_avg.index], rotation=45)
        
        for bar, value in zip(bars3, token_avg.values):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.05,
                    f'{int(value)}', ha='center', fontweight='bold')
        
        # 4. Performance Heatmap
        ax4 = axes[1, 1]
        pivot_data = df.pivot_table(values='time_s', index='strategy', columns='model', aggfunc='mean')
        
        if not pivot_data.empty:
            im = ax4.imshow(pivot_data.values, cmap='RdYlBu_r', aspect='auto')
            ax4.set_xticks(range(len(pivot_data.columns)))
            ax4.set_yticks(range(len(pivot_data.index)))
            ax4.set_xticklabels([col.replace('-', ' ').title() for col in pivot_data.columns])
            ax4.set_yticklabels([idx.replace('_', ' ').title() for idx in pivot_data.index])
            
            # Add values
            for i in range(len(pivot_data.index)):
                for j in range(len(pivot_data.columns)):
                    value = pivot_data.iloc[i, j]
                    ax4.text(j, i, f'{value:.3f}', ha='center', va='center', 
                            fontweight='bold', color='white')
            
            ax4.set_title('Performance Heatmap', fontweight='bold')
            plt.colorbar(im, ax=ax4)
        
        plt.tight_layout()
        
        # Save graph
        graph_path = self.reports_dir / "plots" / f"{problem_set}_performance_analysis.png"
        plt.savefig(graph_path, dpi=300, bbox_inches='tight')
        print(f" Graph saved: {graph_path}")
        plt.close()

    def _generate_statistical_summary(self, df: pd.DataFrame, problem_set: str):
        """Generate statistical summary"""
        summary_lines = []
        summary_lines.append("=" * 80)
        summary_lines.append(" BENCHMARK ANALYSIS REPORT")
        summary_lines.append("=" * 80)
        
        # Strategy ranking
        strategy_ranking = df.groupby('strategy')['time_s'].mean().sort_values()
        summary_lines.append(f"\n STRATEGY PERFORMANCE RANKING:")
        for i, (strategy, time) in enumerate(strategy_ranking.items(), 1):
            summary_lines.append(f"{i}. {strategy.upper().replace('_', ' ')}: {time:.6f}s")
        
        # Model ranking
        model_ranking = df.groupby('model')['time_s'].mean().sort_values()
        summary_lines.append(f"\n MODEL PERFORMANCE RANKING:")
        for i, (model, time) in enumerate(model_ranking.items(), 1):
            summary_lines.append(f"{i}. {model.upper().replace('-', ' ')}: {time:.6f}s")
        
        # Token efficiency
        token_ranking = df.groupby('strategy')['tokens'].mean().sort_values()
        summary_lines.append(f"\n TOKEN EFFICIENCY RANKING:")
        for i, (strategy, tokens) in enumerate(token_ranking.items(), 1):
            summary_lines.append(f"{i}. {strategy.upper().replace('_', ' ')}: {tokens:.1f} tokens")
        
        # Key insights
        summary_lines.append(f"\n KEY INSIGHTS:")
        summary_lines.append(f" Fastest Strategy: {strategy_ranking.index[0].replace('_', ' ').title()}")
        summary_lines.append(f" Fastest Model: {model_ranking.index[0].replace('-', ' ').title()}")
        summary_lines.append(f" Success Rate: {df['success'].mean()*100:.1f}%")
        
        # Best combo
        best_combo = df.loc[df['efficiency_score'].idxmax()]
        summary_lines.append(f" Best Combo: {best_combo['model'].replace('-', ' ').title()} + {best_combo['strategy'].replace('_', ' ').title()}")
        
        summary_lines.append("\n" + "=" * 80)
        
        summary_text = "\n".join(summary_lines)
        print(summary_text)
        
        summary_path = self.reports_dir / f"{problem_set}_analysis_summary.txt"
        with open(summary_path, 'w') as f:
            f.write(summary_text)

    def _save_data(self, df: pd.DataFrame, problem_set: str):
        """Save data to CSV"""
        csv_path = self.reports_dir / "csv" / f"{problem_set}_results.csv"
        df.to_csv(csv_path, index=False)
        print(f" Data saved: {csv_path}")

# Backward compatibility
class ReportGenerator(EnhancedReportGenerator):
    pass

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
import json

class AIOnlyReportGenerator:
    def __init__(self):
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)
        (self.reports_dir / "csv").mkdir(exist_ok=True)
        (self.reports_dir / "plots").mkdir(exist_ok=True)
        
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (16, 10)
        plt.rcParams['font.size'] = 11

    def generate_comprehensive_report(self, results: List[Any], problem_set: str):
        """AI-focused analysis without local-stub"""
        print(f" Generating AI-only analysis for {problem_set}...")
        
        # Extract problem title
        problem_title = self._extract_problem_title(problem_set)
        
        # Create AI-only DataFrame
        df = self._create_ai_only_dataframe(results, problem_set, problem_title)
        
        if df.empty:
            print(" No AI model data to analyze!")
            return
        
        print(f" AI Analysis Dataset:")
        print(f"   Problem: {problem_title}")
        print(f"   Records: {len(df)}")
        print(f"   AI Models: {list(df['model'].unique())}")
        print(f"   Strategies: {list(df['strategy'].unique())}")
        print(f"   Expected: 2 models  5 strategies = 10 combinations")
        
        # Generate AI-focused visualizations
        self._generate_ai_performance_graphs(df, problem_set, problem_title)
        self._generate_ai_statistical_summary(df, problem_set, problem_title)
        self._save_data(df, problem_set)
        
        print(f" AI-focused analysis complete!")

    def _extract_problem_title(self, problem_set: str) -> str:
        """Extract problem title from problem set file"""
        try:
            problem_file = Path(f"data/input/problem_sets/{problem_set}.json")
            
            if problem_file.exists():
                with open(problem_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if 'problems' in data and len(data['problems']) > 0:
                    first_problem = data['problems'][0]
                    title = first_problem.get('title', '')
                    if title:
                        return title
                    problem_id = first_problem.get('id', '')
                    if problem_id:
                        return problem_id.replace('_', ' ').title()
            
            return problem_set.replace('_', ' ').title()
            
        except Exception as e:
            print(f" Could not extract problem title: {e}")
            return problem_set.replace('_', ' ').title()

    def _create_ai_only_dataframe(self, results: List[Any], problem_set: str, problem_title: str) -> pd.DataFrame:
        """Create DataFrame with AI models only - NO local-stub"""
        
        # AI models only
        strategies = ['zero_shot', 'cot', 'few_shot', 'persona', 'template']  
        ai_models = ['starcoder-1b', 'codet5-small']  # NO local-stub
        
        print(f" Processing AI-only results: {len(strategies)} strategies  {len(ai_models)} models = {len(strategies) * len(ai_models)} expected")
        print(f" Total results received: {len(results)}")
        
        data = []
        result_index = 0
        
        # Skip local-stub results (first 5 results are local-stub + all strategies)
        local_stub_results = len(strategies)  # Skip first 5 results
        result_index = local_stub_results  # Start from index 5
        
        print(f" Skipping first {local_stub_results} results (local-stub)")
        
        for strategy in strategies:
            for model in ai_models:
                if result_index < len(results):
                    result = results[result_index]
                    
                    print(f" Processing: {strategy} + {model} (result index {result_index})")
                    
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
                    
                    # Extract generated code
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
                        'problem': problem_title,
                        'problem_id': problem_set,
                        'model': model,
                        'strategy': strategy,
                        'success': success,
                        'time_s': exec_time,
                        'tokens': tokens,
                        'error_message': error_msg,
                        'efficiency_score': self._calculate_ai_efficiency(exec_time, tokens)
                    })
                    
                    result_index += 1
                else:
                    print(f" Missing result for {strategy} + {model}")
        
        df = pd.DataFrame(data)
        print(f" Created AI DataFrame with {len(df)} records")
        return df

    def _calculate_ai_efficiency(self, time_s: float, tokens: int) -> float:
        """Calculate efficiency score optimized for AI model comparison"""
        if not time_s or time_s <= 0:
            return 0.0
        # Balanced efficiency for AI models (both time and token efficiency matter)
        return 1000 / (time_s + (tokens/100))  # Balanced scoring

    def _generate_ai_performance_graphs(self, df: pd.DataFrame, problem_set: str, problem_title: str):
        """Generate AI-focused performance graphs"""
        
        fig, axes = plt.subplots(2, 2, figsize=(18, 12))
        
        # Enhanced title for AI analysis
        fig.suptitle(f'AI Code Generation Analysis: {problem_title}\n', 
                     fontsize=18, fontweight='bold', y=0.96)
        
        # Strategy colors
        strategy_colors = {
            'zero_shot': '#FF6B6B', 'cot': '#4ECDC4', 'few_shot': '#45B7D1',
            'persona': '#96CEB4', 'template': '#FFEAA7'
        }
        
        # AI Model colors  
        ai_model_colors = {
            'starcoder-1b': '#32CD32',    # Lime Green
            'codet5-small': '#4169E1'     # Royal Blue
        }
        
        # 1. AI Strategy Performance
        ax1 = axes[0, 0]
        strategy_avg = df.groupby('strategy')['time_s'].mean().sort_values()
        colors = [strategy_colors.get(s, '#888888') for s in strategy_avg.index]
        bars1 = ax1.bar(range(len(strategy_avg)), strategy_avg.values, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
        
        ax1.set_title('AI Strategy Performance Comparison\n(Lower is Better)', fontweight='bold', pad=15)
        ax1.set_xlabel('Prompt Engineering Strategy', fontweight='bold')
        ax1.set_ylabel('Average Time (seconds)', fontweight='bold')
        ax1.set_xticks(range(len(strategy_avg)))
        ax1.set_xticklabels([s.replace('_', ' ').title() for s in strategy_avg.index], rotation=45, ha='right')
        
        # Add value labels
        for bar, value in zip(bars1, strategy_avg.values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(strategy_avg.values)*0.05,
                    f'{value:.3f}s', ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        ax1.grid(True, alpha=0.3, axis='y')
        
        # 2. AI Model Performance  
        ax2 = axes[0, 1]
        model_avg = df.groupby('model')['time_s'].mean().sort_values()
        colors = [ai_model_colors.get(m, '#888888') for m in model_avg.index]
        bars2 = ax2.bar(range(len(model_avg)), model_avg.values, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
        
        ax2.set_title('AI Model Performance Comparison\n(Lower is Better)', fontweight='bold', pad=15)
        ax2.set_xlabel('AI Code Generation Model', fontweight='bold')
        ax2.set_ylabel('Average Time (seconds)', fontweight='bold')
        ax2.set_xticks(range(len(model_avg)))
        ax2.set_xticklabels([m.replace('-', ' ').title() for m in model_avg.index], rotation=15)
        
        for bar, value in zip(bars2, model_avg.values):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(model_avg.values)*0.05,
                    f'{value:.3f}s', ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 3. Token Efficiency Analysis
        ax3 = axes[1, 0]
        token_avg = df.groupby('strategy')['tokens'].mean().sort_values()
        bars3 = ax3.bar(range(len(token_avg)), token_avg.values, color='lightcoral', alpha=0.8, edgecolor='black', linewidth=1)
        
        ax3.set_title('Token Efficiency by Strategy\n(Lower is More Efficient)', fontweight='bold', pad=15)
        ax3.set_xlabel('Strategy', fontweight='bold')
        ax3.set_ylabel('Average Tokens Generated', fontweight='bold')
        ax3.set_xticks(range(len(token_avg)))
        ax3.set_xticklabels([s.replace('_', ' ').title() for s in token_avg.index], rotation=45, ha='right')
        
        for bar, value in zip(bars3, token_avg.values):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(token_avg.values)*0.05,
                    f'{int(value)}', ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. AI Performance Heatmap
        ax4 = axes[1, 1]
        pivot_data = df.pivot_table(values='time_s', index='strategy', columns='model', aggfunc='mean')
        
        if not pivot_data.empty:
            im = ax4.imshow(pivot_data.values, cmap='RdYlBu_r', aspect='auto')
            ax4.set_xticks(range(len(pivot_data.columns)))
            ax4.set_yticks(range(len(pivot_data.index)))
            ax4.set_xticklabels([col.replace('-', ' ').title() for col in pivot_data.columns], rotation=15)
            ax4.set_yticklabels([idx.replace('_', ' ').title() for idx in pivot_data.index])
            
            # Add values
            for i in range(len(pivot_data.index)):
                for j in range(len(pivot_data.columns)):
                    value = pivot_data.iloc[i, j]
                    if not np.isnan(value):
                        text_color = 'white' if value > pivot_data.values.mean() else 'black'
                        ax4.text(j, i, f'{value:.3f}', ha='center', va='center', 
                                fontweight='bold', fontsize=9, color=text_color)
            
            ax4.set_title('AI Model vs Strategy Heatmap\n(Red=Slower, Blue=Faster)', fontweight='bold', pad=15)
            
            # Add colorbar
            cbar = plt.colorbar(im, ax=ax4, shrink=0.8)
            cbar.set_label('Execution Time (seconds)', rotation=270, labelpad=20)
        
        plt.tight_layout()
        
        # Save with AI-specific filename
        safe_title = problem_title.replace(' ', '_').replace('/', '_')
        graph_path = self.reports_dir / "plots" / f"{safe_title}_AI_analysis.png"
        plt.savefig(graph_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f" AI analysis graph saved: {graph_path}")
        plt.close()

    def _generate_ai_statistical_summary(self, df: pd.DataFrame, problem_set: str, problem_title: str):
        """Generate AI-focused statistical summary"""
        summary_lines = []
        summary_lines.append("=" * 90)
        summary_lines.append(" AI CODE GENERATION BENCHMARK ANALYSIS")
        summary_lines.append("=" * 90)
        summary_lines.append(f" Problem: {problem_title}")
        summary_lines.append(f" Analysis Type: AI Models Only (No Template Systems)")
        summary_lines.append(f" Total AI Experiments: {len(df)}")
        summary_lines.append(f" Models Compared: {', '.join(df['model'].unique())}")
        summary_lines.append(f" Analysis Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # AI Strategy ranking
        strategy_ranking = df.groupby('strategy')['time_s'].mean().sort_values()
        summary_lines.append(f"\n AI STRATEGY EFFECTIVENESS RANKING:")
        for i, (strategy, time) in enumerate(strategy_ranking.items(), 1):
            summary_lines.append(f"{i}. {strategy.upper().replace('_', ' '):<20}: {time:.6f}s average")
        
        # AI Model ranking
        model_ranking = df.groupby('model')['time_s'].mean().sort_values()
        summary_lines.append(f"\n AI MODEL PERFORMANCE RANKING:")
        for i, (model, time) in enumerate(model_ranking.items(), 1):
            summary_lines.append(f"{i}. {model.upper().replace('-', ' '):<20}: {time:.6f}s average")
        
        # Token efficiency for AI
        token_ranking = df.groupby('strategy')['tokens'].mean().sort_values()
        summary_lines.append(f"\n AI TOKEN EFFICIENCY RANKING:")
        for i, (strategy, tokens) in enumerate(token_ranking.items(), 1):
            summary_lines.append(f"{i}. {strategy.upper().replace('_', ' '):<20}: {tokens:.1f} tokens average")
        
        # AI-specific insights
        summary_lines.append(f"\n KEY AI INSIGHTS:")
        summary_lines.append(f"  Best AI Strategy: {strategy_ranking.index[0].replace('_', ' ').title()} ({strategy_ranking.iloc[0]:.6f}s)")
        summary_lines.append(f"  Fastest AI Model: {model_ranking.index[0].replace('-', ' ').title()} ({model_ranking.iloc[0]:.6f}s)")
        summary_lines.append(f"  Most Token Efficient: {token_ranking.index[0].replace('_', ' ').title()} ({token_ranking.iloc[0]:.1f} tokens)")
        summary_lines.append(f"  AI Success Rate: {df['success'].mean()*100:.1f}%")
        
        if len(df) > 0:
            best_ai_combo = df.loc[df['efficiency_score'].idxmax()]
            best_model = best_ai_combo['model'].replace('-', ' ').title()
            best_strategy = best_ai_combo['strategy'].replace('_', ' ').title()
            
            # Performance difference
            fastest = df['time_s'].min()
            slowest = df['time_s'].max()
            performance_range = ((slowest - fastest) / fastest) * 100
            summary_lines.append(f"  Performance Range: {performance_range:.1f}% difference between best and worst AI combinations")
        
        summary_lines.append(f"\n RESEARCH IMPLICATIONS:")
        summary_lines.append(f" This analysis compares only AI models for meaningful insights")
        summary_lines.append(f" Template systems (local-stub) excluded for fair comparison")
        summary_lines.append(f" Results show genuine AI model and strategy effectiveness")
        
        summary_lines.append("\n" + "=" * 90)
        
        summary_text = "\n".join(summary_lines)
        print(summary_text)
        
        # Save with AI-specific filename
        safe_title = problem_title.replace(' ', '_').replace('/', '_')
        summary_path = self.reports_dir / f"{safe_title}_AI_analysis_summary.txt"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_text)
        print(f" AI analysis summary saved: {summary_path}")

    def _save_data(self, df: pd.DataFrame, problem_set: str):
        """Save AI-only data to CSV"""
        csv_path = self.reports_dir / "csv" / f"{problem_set}_AI_only_results.csv"
        df.to_csv(csv_path, index=False)
        print(f" AI-only data saved: {csv_path}")

# Backward compatibility with AI focus
class ReportGenerator(AIOnlyReportGenerator):
    pass

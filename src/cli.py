import click
import os
from .converter import Converter
from .utils import get_default_output_path
from .config import Config

@click.group()
def cli():
    """Markdown to PDF Converter CLI"""
    pass

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', type=click.Path(), help='Output PDF file path')
@click.option('-s', '--style', help='Style theme')
@click.option('--css', type=click.Path(exists=True), help='Custom CSS file path')
@click.option('--toc', is_flag=True, default=False, help='Generate Table of Contents')
@click.option('--config', type=click.Path(exists=True), help='Configuration file path')
def convert(input_file, output, style, css, toc, config):
    """Convert a single Markdown file to PDF"""
    # Load config
    conf = Config().load(config)
    
    # Apply defaults from config if not provided in CLI
    if not style:
        style = conf.get('style', 'github')
    if not toc and conf.get('toc'):
        toc = True
        
    if not output:
        output = get_default_output_path(input_file)
        
    click.echo(f"Converting {input_file} to {output}...")
    
    converter = Converter()
    try:
        converter.convert_file(input_file, output, style=style, css_path=css, toc=toc)
        click.echo(f"Successfully created {output}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False))
@click.option('-o', '--output', type=click.Path(), required=True, help='Output directory')
@click.option('-r', '--recursive', is_flag=True, help='Recursive search')
@click.option('-s', '--style', help='Style theme')
@click.option('--css', type=click.Path(exists=True), help='Custom CSS file path')
@click.option('--toc', is_flag=True, default=False, help='Generate Table of Contents')
@click.option('--config', type=click.Path(exists=True), help='Configuration file path')
@click.option('-w', '--workers', type=int, help='Number of worker processes')
def batch_convert(input_dir, output, recursive, style, css, toc, config, workers):
    """Convert all Markdown files in a directory"""
    # Load config
    conf = Config().load(config)
    
    # Apply defaults from config
    if not style:
        style = conf.get('style', 'github')
    if not toc and conf.get('toc'):
        toc = True
    if not recursive and conf.get('recursive'):
        recursive = True
    if not workers and conf.get('workers'):
        workers = conf.get('workers')

    click.echo(f"Converting files in {input_dir} to {output}...")
    
    converter = Converter()
    results = converter.convert_directory(
        input_dir, output, style=style, css_path=css, recursive=recursive, toc=toc, workers=workers
    )
    
    click.echo(f"Success: {len(results['success'])}")
    click.echo(f"Failed: {len(results['failed'])}")
    
    for failed in results['failed']:
        click.echo(f"  - {failed[0]}: {failed[1]}", err=True)

@cli.command()
def list_styles():
    """List available style themes"""
    from .styles import StyleManager
    manager = StyleManager()
    styles = manager.list_styles()
    click.echo("Available styles:")
    for style in styles:
        click.echo(f"  - {style}")

if __name__ == '__main__':
    cli()
